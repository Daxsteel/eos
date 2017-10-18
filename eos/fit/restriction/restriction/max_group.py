# ==============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2017 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================


from collections import namedtuple

from eos.const.eos import Restriction, State
from eos.const.eve import AttributeId
from eos.fit.item import ModuleHigh, ModuleLow, ModuleMed
from eos.fit.pubsub.message import (
    InstrItemAdd, InstrItemRemove, InstrStatesActivate, InstrStatesDeactivate)
from eos.util.keyed_storage import KeyedStorage
from .base import BaseRestrictionRegister
from ..exception import RestrictionValidationError


TRACKED_ITEM_CLASSES = (ModuleHigh, ModuleMed, ModuleLow)


MaxGroupErrorData = namedtuple(
    'MaxGroupErrorData', ('item_group', 'max_group', 'group_items'))


class MaxGroupRestrictionRegister(BaseRestrictionRegister):
    """Base class for all max modules per group restrictions."""

    def __init__(self, max_group_attr):
        # Attribute ID whose value contains group restriction of item
        self.__max_group_attr = max_group_attr
        # Container for all tracked items, keyed by their group ID
        # Format: {group ID: {items}}
        self.__group_all = KeyedStorage()
        # Container for items, which have max group restriction to become
        # operational
        # Format: {items}
        self.__group_restricted = set()

    def _register_item(self, item):
        if not isinstance(item, TRACKED_ITEM_CLASSES):
            return
        group = item._eve_type.group
        # Ignore items, whose eve type isn't assigned to any group
        if group is None:
            return
        # Having group ID is sufficient condition to enter container of all
        # fitted items
        self.__group_all.add_data_entry(group, item)
        # To enter restriction container, eve type must have restriction
        # attribute
        if self.__max_group_attr not in item._eve_type.attributes:
            return
        self.__group_restricted.add(item)

    def _unregister_item(self, item):
        # Just clear data containers
        group = item._eve_type.group
        self.__group_all.rm_data_entry(group, item)
        self.__group_restricted.discard(item)

    def validate(self):
        # Container for tainted items
        tainted_items = {}
        # Go through all restricted items
        for item in self.__group_restricted:
            # Get number of registered items, assigned to group of current
            # restricted item, and item's restriction value
            group = item._eve_type.group
            group_items = len(self.__group_all.get(group, ()))
            max_group_restriction = (
                item._eve_type.attributes[self.__max_group_attr])
            # If number of registered items from this group is bigger, then
            # current item is tainted
            if group_items > max_group_restriction:
                tainted_items[item] = MaxGroupErrorData(
                    item_group=group,
                    max_group=max_group_restriction,
                    group_items=group_items)
        # Raise error if we detected any tainted items
        if tainted_items:
            raise RestrictionValidationError(tainted_items)


class MaxGroupFittedRestrictionRegister(MaxGroupRestrictionRegister):
    """Prohibit to fit items of certain groups beyond limit.

    Details:
        Only module-class items are restricted.
        For validation, modified value of restriction attribute is taken.
    """

    def __init__(self, msg_broker):
        MaxGroupRestrictionRegister.__init__(self, AttributeId.max_group_fitted)
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_item_addition(self, message):
        MaxGroupRestrictionRegister._register_item(self, message.item)

    def _handle_item_removal(self, message):
        MaxGroupRestrictionRegister._unregister_item(self, message.item)

    _handler_map = {
        InstrItemAdd: _handle_item_addition,
        InstrItemRemove: _handle_item_removal}

    @property
    def type(self):
        return Restriction.max_group_fitted


class MaxGroupOnlineRestrictionRegister(MaxGroupRestrictionRegister):
    """Prohibit to online items of certain groups beyond limit.

    Details:
        Only module-class items are restricted.
        For validation, modified value of restriction attribute is taken.
    """

    def __init__(self, msg_broker):
        MaxGroupRestrictionRegister.__init__(self, AttributeId.max_group_online)
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_item_states_activation(self, message):
        if State.online in message.states:
            MaxGroupRestrictionRegister._register_item(self, message.item)

    def _handle_item_states_deactivation(self, message):
        if State.online in message.states:
            MaxGroupRestrictionRegister._unregister_item(self, message.item)

    _handler_map = {
        InstrStatesActivate: _handle_item_states_activation,
        InstrStatesDeactivate: _handle_item_states_deactivation}

    @property
    def type(self):
        return Restriction.max_group_online


class MaxGroupActiveRestrictionRegister(MaxGroupRestrictionRegister):
    """Prohibit to activate items of certain group beyond limit.

    Details:
        Only module-class items are restricted.
        For validation, modified value of restriction attribute is taken.
    """

    def __init__(self, msg_broker):
        MaxGroupRestrictionRegister.__init__(self, AttributeId.max_group_active)
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_item_states_activation(self, message):
        if State.active in message.states:
            MaxGroupRestrictionRegister._register_item(self, message.item)

    def _handle_item_states_deactivation(self, message):
        if State.active in message.states:
            MaxGroupRestrictionRegister._unregister_item(self, message.item)

    _handler_map = {
        InstrStatesActivate: _handle_item_states_activation,
        InstrStatesDeactivate: _handle_item_states_deactivation}

    @property
    def type(self):
        return Restriction.max_group_active
