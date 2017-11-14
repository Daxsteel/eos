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
from tests.integration.restriction.restriction_testcase import (
    RestrictionTestCase)


class TestTurretSlot(RestrictionTestCase):
    """Check functionality of turret slot quantity restriction."""

    def setUp(self):
        RestrictionTestCase.setUp(self)
        self.ch.attr(attr_id=AttrId.turret_slots_left)
        self.effect = self.ch.effect(
            effect_id=EffectId.turret_fitted,
            category_id=EffectCategoryId.passive)

    def test_fail_excess_single(self):
        # Check that error is raised when quantity of used slots exceeds slot
        # quantity provided by ship
        self.fit.ship = Ship(self.ch.type(
            attrs={AttrId.turret_slots_left: 0}).id)
        item = ModuleHigh(self.ch.type(effects=[self.effect]).id)
        self.fit.modules.high.append(item)
        # Action
        restriction_error = self.get_restriction_error(
            item, Restriction.turret_slot)
        # Verification
        self.assertIsNotNone(restriction_error)
        self.assertEqual(restriction_error.used, 1)
        self.assertEqual(restriction_error.total, 0)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_fail_excess_single_no_ship(self):
        # When stats module does not specify total slot quantity, make sure it's
        # assumed to be 0
        item = ModuleHigh(self.ch.type(effects=[self.effect]).id)
        self.fit.modules.high.append(item)
        # Action
        restriction_error = self.get_restriction_error(
            item, Restriction.turret_slot)
        # Verification
        self.assertIsNotNone(restriction_error)
        self.assertEqual(restriction_error.used, 1)
        self.assertEqual(restriction_error.total, 0)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_fail_excess_multiple(self):
        # Check that error works for multiple items
        self.fit.ship = Ship(self.ch.type(
            attrs={AttrId.turret_slots_left: 1}).id)
        item_type = self.ch.type(effects=[self.effect])
        item1 = ModuleHigh(item_type.id)
        item2 = ModuleHigh(item_type.id)
        self.fit.modules.high.append(item1)
        self.fit.modules.high.append(item2)
        # Action
        restriction_error1 = self.get_restriction_error(
            item1, Restriction.turret_slot)
        # Verification
        self.assertIsNotNone(restriction_error1)
        self.assertEqual(restriction_error1.used, 2)
        self.assertEqual(restriction_error1.total, 1)
        # Action
        restriction_error2 = self.get_restriction_error(
            item2, Restriction.turret_slot)
        # Verification
        self.assertIsNotNone(restriction_error2)
        self.assertEqual(restriction_error2.used, 2)
        self.assertEqual(restriction_error2.total, 1)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_pass_equal(self):
        self.fit.ship = Ship(self.ch.type(
            attrs={AttrId.turret_slots_left: 2}).id)
        item_type = self.ch.type(effects=[self.effect])
        item1 = ModuleHigh(item_type.id)
        item2 = ModuleHigh(item_type.id)
        self.fit.modules.high.append(item1)
        self.fit.modules.high.append(item2)
        # Action
        restriction_error1 = self.get_restriction_error(
            item1, Restriction.turret_slot)
        # Verification
        self.assertIsNone(restriction_error1)
        # Action
        restriction_error2 = self.get_restriction_error(
            item2, Restriction.turret_slot)
        # Verification
        self.assertIsNone(restriction_error2)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_pass_greater(self):
        self.fit.ship = Ship(self.ch.type(
            attrs={AttrId.turret_slots_left: 5}).id)
        item_type = self.ch.type(effects=[self.effect])
        item1 = ModuleHigh(item_type.id)
        item2 = ModuleHigh(item_type.id)
        self.fit.modules.high.append(item1)
        self.fit.modules.high.append(item2)
        # Action
        restriction_error1 = self.get_restriction_error(
            item1, Restriction.turret_slot)
        # Verification
        self.assertIsNone(restriction_error1)
        # Action
        restriction_error2 = self.get_restriction_error(
            item2, Restriction.turret_slot)
        # Verification
        self.assertIsNone(restriction_error2)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_pass_disabled_effect(self):
        self.fit.ship = Ship(self.ch.type(
            attrs={AttrId.turret_slots_left: 0}).id)
        item = ModuleHigh(self.ch.type(effects=[self.effect]).id)
        item.set_effect_mode(self.effect.id, EffectMode.force_stop)
        self.fit.modules.high.append(item)
        # Action
        restriction_error = self.get_restriction_error(
            item, Restriction.turret_slot)
        # Verification
        self.assertIsNone(restriction_error)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_pass_no_source(self):
        self.fit.ship = Ship(self.ch.type(
            attrs={AttrId.turret_slots_left: 0}).id)
        item = ModuleHigh(self.ch.type(effects=[self.effect]).id)
        self.fit.modules.high.append(item)
        self.fit.source = None
        # Action
        restriction_error = self.get_restriction_error(
            item, Restriction.turret_slot)
        # Verification
        self.assertIsNone(restriction_error)
        # Cleanup
        self.assert_fit_buffers_empty(self.fit)
        self.assertEqual(len(self.get_log()), 0)
