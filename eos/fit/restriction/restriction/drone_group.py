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

from eos.const.eos import Restriction
from eos.const.eve import AttrId
from eos.fit.item import Drone, Ship
from eos.fit.message import ItemAdded, ItemRemoved
from .base import BaseRestrictionRegister
from ..exception import RestrictionValidationError


ALLOWED_GROUP_ATTR_IDS = (
    AttrId.allowed_drone_group_1,
    AttrId.allowed_drone_group_2)


DroneGroupErrorData = namedtuple(
    'DroneGroupErrorData', ('group_id', 'allowed_group_ids'))


class DroneGroupRestrictionRegister(BaseRestrictionRegister):
    """Do not allow to use drones besides those specified by ship.

    Details:
        Only items of Drone class are tracked.
        For validation, allowedDroneGroupX attribute values of item type are
            taken.
        If ship specifies no drone group preference, validation always passes.
    """

    def __init__(self, msg_broker):
        self.__current_ship = None
        self.__drones = set()
        msg_broker._subscribe(self, self._handler_map.keys())

    def _handle_item_added(self, msg):
        if isinstance(msg.item, Ship):
            self.__current_ship = msg.item
        elif isinstance(msg.item, Drone):
            self.__drones.add(msg.item)

    def _handle_item_removed(self, msg):
        if msg.item is self.__current_ship:
            self.__current_ship = None
        self.__drones.discard(msg.item)

    _handler_map = {
        ItemAdded: _handle_item_added,
        ItemRemoved: _handle_item_removed}

    def validate(self):
        ship = self.__current_ship
        # No ship - no restriction
        if ship is None:
            return
        allowed_group_ids = []
        # Find out if we have restriction, and which drone groups it allows
        for allowed_group_attr_id in ALLOWED_GROUP_ATTR_IDS:
            try:
                allowed_group_id = ship._type_attrs[allowed_group_attr_id]
            except KeyError:
                continue
            else:
                allowed_group_ids.append(allowed_group_id)
        # No allowed group attributes - no restriction
        if not allowed_group_ids:
            return
        tainted_items = {}
        # Convert set to tuple, this way we can use it multiple times in error
        # data, making sure that it can't be modified by validation caller
        allowed_group_ids = tuple(allowed_group_ids)
        for drone in self.__drones:
            # Taint items, whose group is not allowed
            group_id = drone._type.group_id
            if group_id not in allowed_group_ids:
                tainted_items[drone] = DroneGroupErrorData(
                    group_id=group_id,
                    allowed_group_ids=allowed_group_ids)
        if tainted_items:
            raise RestrictionValidationError(tainted_items)

    @property
    def type(self):
        return Restriction.drone_group
