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


class TestItemDmgTurret(ItemMixinTestCase):

    def setUp(self):
        ItemMixinTestCase.setUp(self)
        self.mkattr(attr_id=AttrId.capacity)
        self.mkattr(attr_id=AttrId.volume)
        self.mkattr(attr_id=AttrId.charge_rate)
        self.mkattr(attr_id=AttrId.reload_time)
        self.mkattr(attr_id=AttrId.dmg_multiplier)
        self.mkattr(attr_id=AttrId.em_dmg)
        self.mkattr(attr_id=AttrId.thermal_dmg)
        self.mkattr(attr_id=AttrId.kinetic_dmg)
        self.mkattr(attr_id=AttrId.explosive_dmg)
        self.cycle_attr = self.mkattr()
        self.effect = self.mkeffect(
            effect_id=EffectId.projectile_fired,
            category_id=EffectCategoryId.active,
            duration_attr_id=self.cycle_attr.id)

    def test_nominal_volley_generic(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.active)
        item.charge = Charge(self.mktype(attrs={
            AttrId.volume: 0.2,
            AttrId.em_dmg: 5.2,
            AttrId.thermal_dmg: 6.3,
            AttrId.kinetic_dmg: 7.4,
            AttrId.explosive_dmg: 8.5}).id)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 13)
        self.assertAlmostEqual(volley.thermal, 15.75)
        self.assertAlmostEqual(volley.kinetic, 18.5)
        self.assertAlmostEqual(volley.explosive, 21.25)
        self.assertAlmostEqual(volley.total, 68.5)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_no_multiplier(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.active)
        item.charge = Charge(self.mktype(attrs={
            AttrId.volume: 0.2,
            AttrId.em_dmg: 5.2,
            AttrId.thermal_dmg: 6.3,
            AttrId.kinetic_dmg: 7.4,
            AttrId.explosive_dmg: 8.5}).id)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 5.2)
        self.assertAlmostEqual(volley.thermal, 6.3)
        self.assertAlmostEqual(volley.kinetic, 7.4)
        self.assertAlmostEqual(volley.explosive, 8.5)
        self.assertAlmostEqual(volley.total, 27.4)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_volley_insufficient_state(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.online)
        item.charge = Charge(self.mktype(attrs={
            AttrId.volume: 0.2,
            AttrId.em_dmg: 5.2,
            AttrId.thermal_dmg: 6.3,
            AttrId.kinetic_dmg: 7.4,
            AttrId.explosive_dmg: 8.5}).id)
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

    def test_nominal_volley_disabled_effect(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.active)
        item.set_effect_mode(self.effect.id, EffectMode.force_stop)
        item.charge = Charge(self.mktype(attrs={
            AttrId.volume: 0.2,
            AttrId.em_dmg: 5.2,
            AttrId.thermal_dmg: 6.3,
            AttrId.kinetic_dmg: 7.4,
            AttrId.explosive_dmg: 8.5}).id)
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
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
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

    def test_nominal_volley_onitem_dmg_stats(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.em_dmg: 5.2,
                    AttrId.thermal_dmg: 6.3,
                    AttrId.kinetic_dmg: 7.4,
                    AttrId.explosive_dmg: 8.5, self.cycle_attr.id: 500},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.active)
        fit.modules.high.append(item)
        # Verification
        volley = item.get_nominal_volley()
        self.assertAlmostEqual(volley.em, 13)
        self.assertAlmostEqual(volley.thermal, 15.75)
        self.assertAlmostEqual(volley.kinetic, 18.5)
        self.assertAlmostEqual(volley.explosive, 21.25)
        self.assertAlmostEqual(volley.total, 68.5)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_dps_no_reload(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.active)
        item.charge = Charge(self.mktype(attrs={
            AttrId.volume: 0.2,
            AttrId.em_dmg: 5.2,
            AttrId.thermal_dmg: 6.3,
            AttrId.kinetic_dmg: 7.4,
            AttrId.explosive_dmg: 8.5}).id)
        fit.modules.high.append(item)
        # Verification
        dps = item.get_nominal_dps(reload=False)
        self.assertAlmostEqual(dps.em, 26)
        self.assertAlmostEqual(dps.thermal, 31.5)
        self.assertAlmostEqual(dps.kinetic, 37)
        self.assertAlmostEqual(dps.explosive, 42.5)
        self.assertAlmostEqual(dps.total, 137)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_nominal_dps_reload(self):
        fit = Fit()
        item = ModuleHigh(
            self.mktype(
                attrs={
                    AttrId.dmg_multiplier: 2.5,
                    AttrId.capacity: 2.0,
                    self.cycle_attr.id: 500,
                    AttrId.charge_rate: 1.0,
                    AttrId.reload_time: 5000},
                effects=[self.effect],
                default_effect=self.effect).id,
            state=State.active)
        item.charge = Charge(self.mktype(attrs={
            AttrId.volume: 0.2,
            AttrId.em_dmg: 5.2,
            AttrId.thermal_dmg: 6.3,
            AttrId.kinetic_dmg: 7.4,
            AttrId.explosive_dmg: 8.5}).id)
        fit.modules.high.append(item)
        # Verification
        dps = item.get_nominal_dps(reload=True)
        self.assertAlmostEqual(dps.em, 13)
        self.assertAlmostEqual(dps.thermal, 15.75)
        self.assertAlmostEqual(dps.kinetic, 18.5)
        self.assertAlmostEqual(dps.explosive, 21.25)
        self.assertAlmostEqual(dps.total, 68.5)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)
