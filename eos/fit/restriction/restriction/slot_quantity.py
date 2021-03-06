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
from .base import BaseRestriction
from ..exception import RestrictionValidationError


SlotQuantityErrorData = namedtuple(
    'SlotQuantityErrorData', ('used', 'total'))


class OrderedSlotRestriction(BaseRestriction):
    """Base class for all ordered slot quantity restrictions."""

    def __init__(self, stats, stat_name):
        self.__stats = stats
        self.__stat_name = stat_name

    def validate(self):
        # Use stats module to get max and used quantity of slots
        stats = getattr(self.__stats, self.__stat_name)
        used = stats.used
        # Can be None, so fall back to 0 in this case
        total = stats.total or 0
        # If quantity of items which take this slot is bigger than quantity of
        # available slots, then all items which are positioned higher than
        # available index are tainted
        if used > total:
            tainted_items = {}
            for item in stats._users:
                position = item._container_position
                if position is not None and position + 1 > total:
                    tainted_items[item] = SlotQuantityErrorData(
                        used=used, total=total)
            raise RestrictionValidationError(tainted_items)


class UnorderedSlotRestriction(BaseRestriction):
    """Base class for all unordered slot quantity restrictions."""

    def __init__(self, stats, stat_name):
        self.__stats = stats
        self.__stat_name = stat_name

    def validate(self):
        stats = getattr(self.__stats, self.__stat_name)
        used = stats.used
        total = stats.total or 0
        # If quantity of items which take this slot is bigger than quantity of
        # available slots, then all items which use this slot are tainted
        if used > total:
            tainted_items = {}
            for item in stats._users:
                tainted_items[item] = SlotQuantityErrorData(
                    used=used, total=total)
            raise RestrictionValidationError(tainted_items)


class HighSlotRestriction(OrderedSlotRestriction):
    """Quantity of high-slot items should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        OrderedSlotRestriction.__init__(self, stats, 'high_slots')

    @property
    def type(self):
        return Restriction.high_slot


class MediumSlotRestriction(OrderedSlotRestriction):
    """Quantity of med-slot items should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        OrderedSlotRestriction.__init__(self, stats, 'med_slots')

    @property
    def type(self):
        return Restriction.medium_slot


class LowSlotRestriction(OrderedSlotRestriction):
    """Quantity of low-slot items should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        OrderedSlotRestriction.__init__(self, stats, 'low_slots')

    @property
    def type(self):
        return Restriction.low_slot


class RigSlotRestriction(UnorderedSlotRestriction):
    """Quantity of rig items should not exceed limit.

    Details:
        For validation, stats module data is used.
    """
    def __init__(self, stats):
        UnorderedSlotRestriction.__init__(self, stats, 'rig_slots')

    @property
    def type(self):
        return Restriction.rig_slot


class SubsystemSlotRestriction(UnorderedSlotRestriction):
    """Quantity of subsystem items should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        UnorderedSlotRestriction.__init__(self, stats, 'subsystem_slots')

    @property
    def type(self):
        return Restriction.subsystem_slot


class TurretSlotRestriction(UnorderedSlotRestriction):
    """Quantity of turrets should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        UnorderedSlotRestriction.__init__(self, stats, 'turret_slots')

    @property
    def type(self):
        return Restriction.turret_slot


class LauncherSlotRestriction(UnorderedSlotRestriction):
    """Quantity of launchers should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        UnorderedSlotRestriction.__init__(self, stats, 'launcher_slots')

    @property
    def type(self):
        return Restriction.launcher_slot


class LaunchedDroneRestriction(UnorderedSlotRestriction):
    """Quantity of launched drones should not exceed limit.

    Details:
        For validation, stats module data is used.
    """

    def __init__(self, stats):
        UnorderedSlotRestriction.__init__(self, stats, 'launched_drones')

    @property
    def type(self):
        return Restriction.launched_drone
