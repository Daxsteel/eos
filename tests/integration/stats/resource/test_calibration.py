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
from tests.integration.stats.stats_testcase import StatsTestCase


class TestCalibration(StatsTestCase):

    def setUp(self):
        StatsTestCase.setUp(self)
        self.mkattr(attr_id=AttrId.upgrade_capacity)
        self.mkattr(attr_id=AttrId.upgrade_cost)
        self.effect = self.mkeffect(
            effect_id=EffectId.rig_slot,
            category_id=EffectCategoryId.passive)

    def test_output(self):
        # Check that modified attribute of ship is used
        self.fit.ship = Ship(self.mktype(
            attrs={AttrId.upgrade_capacity: 350}).id)
        # Verification
        self.assertAlmostEqual(self.fit.stats.calibration.output, 350)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_output_no_ship(self):
        # None for output when no ship
        # Verification
        self.assertIsNone(self.fit.stats.calibration.output)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_output_no_attr(self):
        # None for output when no attribute on ship
        self.fit.ship = Ship(self.mktype().id)
        # Verification
        self.assertIsNone(self.fit.stats.calibration.output)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_use_single_no_rounding(self):
        self.fit.rigs.add(Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 55.5555555555},
            effects=[self.effect]).id))
        # Verification
        self.assertAlmostEqual(self.fit.stats.calibration.used, 55.5555555555)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_use_multiple(self):
        self.fit.rigs.add(Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 50},
            effects=[self.effect]).id))
        self.fit.rigs.add(Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 30},
            effects=[self.effect]).id))
        # Verification
        self.assertAlmostEqual(self.fit.stats.calibration.used, 80)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_use_disabled_effect(self):
        item1 = Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 50},
            effects=[self.effect]).id)
        item2 = Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 30},
            effects=[self.effect]).id)
        item2.set_effect_mode(self.effect.id, EffectMode.force_stop)
        self.fit.rigs.add(item1)
        self.fit.rigs.add(item2)
        # Verification
        self.assertAlmostEqual(self.fit.stats.calibration.used, 50)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_use_none(self):
        # Verification
        self.assertAlmostEqual(self.fit.stats.calibration.used, 0)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_no_source(self):
        self.fit.ship = Ship(self.mktype(
            attrs={AttrId.upgrade_capacity: 350}).id)
        self.fit.rigs.add(Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 50},
            effects=[self.effect]).id))
        self.fit.rigs.add(Rig(self.mktype(
            attrs={AttrId.upgrade_cost: 30},
            effects=[self.effect]).id))
        self.fit.source = None
        # Verification
        self.assertAlmostEqual(self.fit.stats.calibration.used, 0)
        self.assertIsNone(self.fit.stats.calibration.output)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)
