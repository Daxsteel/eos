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


from eos.const.eve import EffectId
from .ancillary_armor_repairer import add_aar_modifier
from .online_effect_category import fix_online_category
from .propulsion_modules import add_ab_modifiers, add_mwd_modifiers
from .reactive_armor_hardener import add_rah_modifiers


# Format: {effect ID: customization method}
_effect_id_map = {
    EffectId.adaptive_armor_hardener: add_rah_modifiers,
    EffectId.fueled_armor_repair: add_aar_modifier,
    EffectId.module_bonus_afterburner: add_ab_modifiers,
    EffectId.module_bonus_ancillary_remote_armor_repairer: add_aar_modifier,
    EffectId.module_bonus_microwarpdrive: add_mwd_modifiers,
    EffectId.online: fix_online_category}


def customize_effect(effect):
    if effect.id in _effect_id_map:
        _effect_id_map[effect.id](effect)
