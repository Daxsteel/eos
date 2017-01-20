# ===============================================================================
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
# ===============================================================================


__all__ = [
    'ItemModifier',
    'LocationModifier',
    'LocationGroupModifier',
    'LocationRequiredSkillModifier',
    'OwnerRequiredSkillModifier'
]


from eos.const.eos import ModifierType

from .item import ItemModifier
from .location import LocationModifier
from .location_group import LocationGroupModifier
from .location_skillrq import LocationRequiredSkillModifier
from .owner_skillrq import OwnerRequiredSkillModifier


mod_map = {
    ModifierType.item: ItemModifier,
    ModifierType.location: LocationModifier,
    ModifierType.group: LocationGroupModifier,
    ModifierType.location_skillrq: LocationRequiredSkillModifier,
    ModifierType.owner_skillrq: OwnerRequiredSkillModifier
}


def unpackage_modifier(mod_id, mod_type, *args):
    return mod_map[mod_type](mod_id, *args)
