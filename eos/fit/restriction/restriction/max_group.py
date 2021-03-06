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
from eos.const.eve import AttrId
from eos.fit.item import ModuleHigh, ModuleLow, ModuleMed
from eos.fit.message import (
    ItemAdded, ItemRemoved, StatesActivated, StatesDeactivated)
from eos.util.keyed_storage import KeyedStorage
from .base import BaseRestrictionRegister
from ..exception import RestrictionValidationError


TRACKED_ITEM_CLASSES = (ModuleHigh, ModuleMed, ModuleLow)


MaxGroupErrorData = namedtuple(
    'MaxGroupErrorData', ('group_id', 'quantity', 'max_allowed_quantity'))


class MaxGroupRestrictionRegister(BaseRestrictionRegister):
    """Base class for all max modules per group restrictions."""

    def __init__(self, max_group_attr_id):
        # Attribute ID whose value contains group restriction of item
        self.__max_group_attr_id = max_group_attr_id
        # Container for all tracked items, keyed by their group ID
        # Format: {group ID: {items}}
        self.__group_item_map = KeyedStorage()
        # Container for items, which have max group restriction to become
        # operational
        # Format: {items}
        self.__restricted_items = set()

    def _register_item(self, item):
        if not isinstance(item, TRACKED_ITEM_CLASSES):
            return
        group_id = item._type.group_id
        # Ignore items, whose type isn't assigned to any group
        if group_id is None:
            return
        # Having group ID is sufficient condition to enter container of all
        # fitted items
        self.__group_item_map.add_data_entry(group_id, item)
        # To enter restriction container, item's type must have restriction
        # attribute
        if self.__max_group_attr_id not in item._type_attrs:
            return
        self.__restricted_items.add(item)

    def _unregister_item(self, item):
        # Just clear data containers
        group_id = item._type.group_id
        self.__group_item_map.rm_data_entry(group_id, item)
        self.__restricted_items.discard(item)

    def validate(self):
        # Container for tainted items
        tainted_items = {}
        # Go through all restricted items
        for item in self.__restricted_items:
            # Get quantity of registered items, assigned to group of current
            # restricted item, and item's restriction value
            group_id = item._type.group_id
            quantity = len(self.__group_item_map.get(group_id, ()))
            max_allowed_quantity = item._type_attrs[self.__max_group_attr_id]
            if quantity > max_allowed_quantity:
                tainted_items[item] = MaxGroupErrorData(
                    group_id=group_id,
                    quantity=quantity,
                    max_allowed_quantity=max_allowed_quantity)
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
        MaxGroupRestrictionRegister.__init__(self, AttrId.max_group_fitted)
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_item_added(self, msg):
        MaxGroupRestrictionRegister._register_item(self, msg.item)

    def _handle_item_removed(self, msg):
        MaxGroupRestrictionRegister._unregister_item(self, msg.item)

    _handler_map = {
        ItemAdded: _handle_item_added,
        ItemRemoved: _handle_item_removed}

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
        MaxGroupRestrictionRegister.__init__(self, AttrId.max_group_online)
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_states_activated(self, msg):
        if State.online in msg.states:
            MaxGroupRestrictionRegister._register_item(self, msg.item)

    def _handle_states_deactivated(self, msg):
        if State.online in msg.states:
            MaxGroupRestrictionRegister._unregister_item(self, msg.item)

    _handler_map = {
        StatesActivated: _handle_states_activated,
        StatesDeactivated: _handle_states_deactivated}

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
        MaxGroupRestrictionRegister.__init__(self, AttrId.max_group_active)
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_states_activated(self, msg):
        if State.active in msg.states:
            MaxGroupRestrictionRegister._register_item(self, msg.item)

    def _handle_states_deactivated(self, msg):
        if State.active in msg.states:
            MaxGroupRestrictionRegister._unregister_item(self, msg.item)

    _handler_map = {
        StatesActivated: _handle_states_activated,
        StatesDeactivated: _handle_states_deactivated}

    @property
    def type(self):
        return Restriction.max_group_active
