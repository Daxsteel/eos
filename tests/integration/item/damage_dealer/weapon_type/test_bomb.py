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


from eos import *
from eos.const.eve import AttrId, EffectId, EffectCategoryId
from tests.integration.item.item_testcase import ItemMixinTestCase


class TestItemDmgBomb(ItemMixinTestCase):

    def setUp(self):
        ItemMixinTestCase.setUp(self)
        self.mkattr(attr_id=AttrId.capacity)
        self.mkattr(attr_id=AttrId.volume)
        self.mkattr(attr_id=AttrId.charge_rate)
        self.mkattr(attr_id=AttrId.reload_time)
        self.mkattr(attr_id=AttrId.module_reactivation_delay)
        self.mkattr(attr_id=AttrId.em_dmg)
        self.mkattr(attr_id=AttrId.thermal_dmg)
        self.mkattr(attr_id=AttrId.kinetic_dmg)
        self.mkattr(attr_id=AttrId.explosive_dmg)
        self.cycle_attr = self.mkattr()
        self.effect_item = self.mkeffect(
            effect_id=EffectId.use_missiles,
            category_id=EffectCategoryId.active,
            duration_attr_id=self.cycle_attr.id)
        self.effect_charge = self.mkeffect(
            effect_id=EffectId.bomb_launching,
            category_id=EffectCategoryId.passive)

    def test_nominal_volley_generic(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5200)
        self.assertAlmostEqual(volley.thermal, 6300)
        self.assertAlmostEqual(volley.kinetic, 7400)
        self.assertAlmostEqual(volley.explosive, 8500)
        self.assertAlmostEqual(volley.total, 27400)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_volley_multiplier(self):
        self.mkattr(attr_id=AttrId.dmg_multiplier)
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000,
                    AttrId.dmg_multiplier: 5.5},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5200)
        self.assertAlmostEqual(volley.thermal, 6300)
        self.assertAlmostEqual(volley.kinetic, 7400)
        self.assertAlmostEqual(volley.explosive, 8500)
        self.assertAlmostEqual(volley.total, 27400)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_volley_insufficient_state(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.online)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertIsNone(volley.em)
        self.assertIsNone(volley.thermal)
        self.assertIsNone(volley.kinetic)
        self.assertIsNone(volley.explosive)
        self.assertIsNone(volley.total)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_volley_disabled_item_effect(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        item.set_effect_mode(self.effect_item.id, EffectMode.force_stop)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertIsNone(volley.em)
        self.assertIsNone(volley.thermal)
        self.assertIsNone(volley.kinetic)
        self.assertIsNone(volley.explosive)
        self.assertIsNone(volley.total)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_volley_disabled_charge_effect(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        item.charge.set_effect_mode(
            self.effect_charge.id, EffectMode.force_stop)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertIsNone(volley.em)
        self.assertIsNone(volley.thermal)
        self.assertIsNone(volley.kinetic)
        self.assertIsNone(volley.explosive)
        self.assertIsNone(volley.total)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_volley_no_charge(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertIsNone(volley.em)
        self.assertIsNone(volley.thermal)
        self.assertIsNone(volley.kinetic)
        self.assertIsNone(volley.explosive)
        self.assertIsNone(volley.total)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_dps_no_reload(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        fit.modules.high.append(item)
        # Verification
        dps = item.get_nominal_dps(reload=False)
        self.assertAlmostEqual(dps.em, 41.6)
        self.assertAlmostEqual(dps.thermal, 50.4)
        self.assertAlmostEqual(dps.kinetic, 59.2)
        self.assertAlmostEqual(dps.explosive, 68)
        self.assertAlmostEqual(dps.total, 219.2)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_dps_reload(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 60.0,
                    self.cycle_attr.id: 5000,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 10000,
                    AttrId.module_reactivation_delay: 120000},
                effects=[self.effect_item],
                default_effect=self.effect_item).id,
            state=State.active)
        item.charge = Charge(self.mktype(
            attrs={
                AttrId.volume: 30.0,
                AttrId.em_dmg: 5200,
                AttrId.thermal_dmg: 6300,
                AttrId.kinetic_dmg: 7400,
                AttrId.explosive_dmg: 8500},
            effects=[self.effect_charge],
            default_effect=self.effect_charge).id)
        fit.modules.high.append(item)
        # Verification
        dps = item.get_nominal_dps(reload=True)
        # Reload doesn't affect DPS because reactivation time is higher, item
        # manages to reload during that time
        self.assertAlmostEqual(dps.em, 41.6)
        self.assertAlmostEqual(dps.thermal, 50.4)
        self.assertAlmostEqual(dps.kinetic, 59.2)
        self.assertAlmostEqual(dps.explosive, 68)
        self.assertAlmostEqual(dps.total, 219.2)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)
