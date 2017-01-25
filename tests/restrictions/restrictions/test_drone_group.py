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


from unittest.mock import Mock

from eos.const.eos import ModifierDomain, Restriction, State
from eos.const.eve import Attribute
from eos.fit.item import Drone, Ship, Implant
from tests.restrictions.restriction_testcase import RestrictionTestCase


class TestDroneGroup(RestrictionTestCase):
    """Check functionality of drone group restriction"""

    def test_fail_mismatch1(self):
        # Check that error is returned on attempt
        # to add drone from group mismatching to
        # first restriction attribute
        eve_type = self.ch.type_(type_id=1, group=56)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_1: 4})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNotNone(restriction_error)
        self.assertCountEqual(restriction_error.allowed_groups, (4,))
        self.assertEqual(restriction_error.holder_group, 56)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_fail_mismatch2(self):
        # Check that error is returned on attempt
        # to add drone from group mismatching to
        # second restriction attribute
        eve_type = self.ch.type_(type_id=1, group=797)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_2: 69})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNotNone(restriction_error)
        self.assertCountEqual(restriction_error.allowed_groups, (69,))
        self.assertEqual(restriction_error.holder_group, 797)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_fail_mismatch_combined(self):
        # Check that error is returned on attempt
        # to add drone from group mismatching to
        # both restriction attributes
        eve_type = self.ch.type_(type_id=1, group=803)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(
            type_id=2, attributes={Attribute.allowed_drone_group_1: 48, Attribute.allowed_drone_group_2: 106})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNotNone(restriction_error)
        self.assertCountEqual(restriction_error.allowed_groups, (48, 106))
        self.assertEqual(restriction_error.holder_group, 803)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_fail_mismatch_attr_eve_type(self):
        # Check that error is returned on attempt
        # to add drone from group mismatching to
        # EVE type restriction attribute, but matching
        # to modified restriction attribute. Effectively
        # we check that EVE type attribute value is taken
        eve_type = self.ch.type_(type_id=1, group=37)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_1: 59})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        ship_holder.attributes = {Attribute.allowed_drone_group_1: 37}
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNotNone(restriction_error)
        self.assertCountEqual(restriction_error.allowed_groups, (59,))
        self.assertEqual(restriction_error.holder_group, 37)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_fail_drone_none(self):
        # Check that drone from None group is subject
        # to restriction
        eve_type = self.ch.type_(type_id=1, group=None)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_1: 1896})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNotNone(restriction_error)
        self.assertCountEqual(restriction_error.allowed_groups, (1896,))
        self.assertEqual(restriction_error.holder_group, None)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_pass_no_ship(self):
        # Check that restriction isn't applied
        # when fit doesn't have ship
        eve_type = self.ch.type_(type_id=1, group=None)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNone(restriction_error)
        self.remove_holder(holder)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_pass_ship_no_restriction(self):
        # Check that restriction isn't applied
        # when fit has ship, but without restriction
        # attribute
        eve_type = self.ch.type_(type_id=1, group=71)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2)
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNone(restriction_error)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_pass_non_drone(self):
        # Check that restriction is not applied
        # to holders which are not drones
        eve_type = self.ch.type_(type_id=1, group=56)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=ModifierDomain.character, spec_set=Implant(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_1: 4})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNone(restriction_error)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_pass_match1(self):
        # Check that no error raised when drone of group
        # matching to first restriction attribute is added
        eve_type = self.ch.type_(type_id=1, group=22)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_1: 22})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNone(restriction_error)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_pass_match2(self):
        # Check that no error raised when drone of group
        # matching to second restriction attribute is added
        eve_type = self.ch.type_(type_id=1, group=67)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(type_id=2, attributes={Attribute.allowed_drone_group_2: 67})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNone(restriction_error)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()

    def test_pass_match_combination(self):
        # Check that no error raised when drone of group
        # matching to any of two restriction attributes
        # is added
        eve_type = self.ch.type_(type_id=1, group=53)
        holder = Mock(state=State.offline, _eve_type=eve_type, _domain=None, spec_set=Drone(1))
        self.add_holder(holder)
        ship_eve_type = self.ch.type_(
            type_id=2, attributes={Attribute.allowed_drone_group_1: 907, Attribute.allowed_drone_group_2: 53})
        ship_holder = Mock(state=State.offline, _eve_type=ship_eve_type, _domain=None, spec_set=Ship(1))
        self.set_ship(ship_holder)
        restriction_error = self.get_restriction_error(holder, Restriction.drone_group)
        self.assertIsNone(restriction_error)
        self.remove_holder(holder)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_restriction_buffers_empty()
