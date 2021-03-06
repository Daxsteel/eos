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
from eos.const.eve import AttrId
from tests.integration.item.item_testcase import ItemMixinTestCase


class TestItemMixinChargeQuantity(ItemMixinTestCase):

    def setUp(self):
        ItemMixinTestCase.setUp(self)
        self.mkattr(attr_id=AttrId.capacity)
        self.mkattr(attr_id=AttrId.volume)

    def test_generic(self):
        fit = Fit()
        item = ModuleHigh(self.mktype(attrs={AttrId.capacity: 20.0}).id)
        item.charge = Charge(self.mktype(attrs={AttrId.volume: 2.0}).id)
        fit.modules.high.append(item)
        # Verification
        self.assertEqual(item.charge_quantity, 10)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_float_error(self):
        fit = Fit()
        item = ModuleHigh(self.mktype(attrs={AttrId.capacity: 2.3}).id)
        item.charge = Charge(self.mktype(attrs={AttrId.volume: 0.1}).id)
        fit.modules.high.append(item)
        # Verification
        self.assertEqual(item.charge_quantity, 23)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_round_down(self):
        fit = Fit()
        item = ModuleHigh(self.mktype(attrs={AttrId.capacity: 19.7}).id)
        item.charge = Charge(self.mktype(attrs={AttrId.volume: 2.0}).id)
        fit.modules.high.append(item)
        # Verification
        self.assertEqual(item.charge_quantity, 9)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_no_volume(self):
        fit = Fit()
        item = ModuleHigh(self.mktype(attrs={AttrId.capacity: 20.0}).id)
        item.charge = Charge(self.mktype().id)
        fit.modules.high.append(item)
        # Verification
        self.assertIsNone(item.charge_quantity)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_no_capacity(self):
        fit = Fit()
        item = ModuleHigh(self.mktype().id)
        item.charge = Charge(self.mktype(attrs={AttrId.volume: 2.0}).id)
        fit.modules.high.append(item)
        # Verification
        self.assertIsNone(item.charge_quantity)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_no_charge(self):
        fit = Fit()
        item = ModuleHigh(self.mktype(attrs={AttrId.capacity: 20.0}).id)
        fit.modules.high.append(item)
        # Verification
        self.assertIsNone(item.charge_quantity)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_no_source(self):
        fit = Fit()
        item = ModuleHigh(self.mktype(attrs={AttrId.capacity: 20.0}).id)
        item.charge = Charge(self.mktype(attrs={AttrId.volume: 2.0}).id)
        fit.modules.high.append(item)
        fit.source = None
        # Verification
        self.assertIsNone(item.charge_quantity)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)
