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
from eos.const.eos import ModDomain, ModOperator, ModTgtFilter
from eos.const.eve import EffectCategoryId
from tests.integration.item.item_testcase import ItemMixinTestCase


class TestItemMixinSideEffect(ItemMixinTestCase):

    def test_data(self):
        # Setup
        chance_attr1 = self.mkattr()
        chance_attr2 = self.mkattr()
        src_attr = self.mkattr()
        modifier = self.mkmod(
            tgt_filter=ModTgtFilter.item,
            tgt_domain=ModDomain.self,
            tgt_attr_id=chance_attr2.id,
            operator=ModOperator.post_percent,
            src_attr_id=src_attr.id)
        effect1 = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr1.id)
        effect2 = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr2.id)
        effect3 = self.mkeffect(
            category_id=EffectCategoryId.passive,
            modifiers=[modifier])
        fit = Fit()
        item = Booster(self.mktype(
            attrs={
                chance_attr1.id: 0.5,
                chance_attr2.id: 0.1,
                src_attr.id: -25},
            effects=(effect1, effect2, effect3)).id)
        fit.boosters.add(item)
        item.set_side_effect_status(effect2.id, True)
        # Verification
        side_effects = item.side_effects
        self.assertEqual(len(side_effects), 2)
        self.assertIn(effect1.id, side_effects)
        side_effect1 = side_effects[effect1.id]
        self.assertIs(side_effect1.effect, effect1)
        self.assertAlmostEqual(side_effect1.chance, 0.5)
        self.assertIs(side_effect1.status, False)
        self.assertIn(effect2.id, side_effects)
        side_effect2 = side_effects[effect2.id]
        self.assertIs(side_effect2.effect, effect2)
        self.assertAlmostEqual(side_effect2.chance, 0.075)
        self.assertIs(side_effect2.status, True)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_data_no_source(self):
        # Setup
        chance_attr1 = self.mkattr()
        chance_attr2 = self.mkattr()
        src_attr = self.mkattr()
        modifier = self.mkmod(
            tgt_filter=ModTgtFilter.item,
            tgt_domain=ModDomain.self,
            tgt_attr_id=chance_attr2.id,
            operator=ModOperator.post_percent,
            src_attr_id=src_attr.id)
        effect1 = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr1.id)
        effect2 = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr2.id)
        effect3 = self.mkeffect(
            category_id=EffectCategoryId.passive,
            modifiers=[modifier])
        fit = Fit(source=None)
        item = Booster(self.mktype(
            attrs={
                chance_attr1.id: 0.5,
                chance_attr2.id: 0.1,
                src_attr.id: -25},
            effects=(effect1, effect2, effect3)).id)
        fit.boosters.add(item)
        item.set_side_effect_status(effect2.id, True)
        # Verification
        side_effects = item.side_effects
        self.assertEqual(len(side_effects), 0)
        self.assertNotIn(effect1.id, side_effects)
        self.assertNotIn(effect2.id, side_effects)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_persistence(self):
        # Here we check that when item type doesn't have effect which was
        # disabled anymore, everything runs as expected, and when this effect
        # appears again - it's disabled
        # Setup
        chance_attr1_id = self.allocate_attr_id('src1', 'src2')
        self.mkattr(src='src1', attr_id=chance_attr1_id)
        self.mkattr(src='src2', attr_id=chance_attr1_id)
        chance_attr2 = self.mkattr(src='src1')
        chance_attr3 = self.mkattr(src='src1')
        # 1st effect exists as side-effect in both sources
        effect1_id = self.allocate_effect_id('src1', 'src2')
        effect1_src1 = self.mkeffect(
            src='src1',
            effect_id=effect1_id,
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr1_id)
        effect1_src2 = self.mkeffect(
            src='src2',
            effect_id=effect1_id,
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr1_id)
        # 2nd effect exists as side-effect in src1, and as regular effect in
        # src2
        effect2_id = self.allocate_effect_id('src1', 'src2')
        effect2_src1 = self.mkeffect(
            src='src1',
            effect_id=effect2_id,
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr2.id)
        effect2_src2 = self.mkeffect(
            src='src2',
            effect_id=effect2_id,
            category_id=EffectCategoryId.passive)
        # 3rd effect exists as side-effect in src1 and doesn't exist in src2 at
        # all
        effect3_id = self.allocate_effect_id('src1', 'src2')
        effect3_src1 = self.mkeffect(
            src='src1',
            effect_id=effect3_id,
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr3.id)
        item_type_id = self.allocate_type_id('src1', 'src2')
        self.mktype(
            src='src1',
            type_id=item_type_id,
            attrs={
                chance_attr1_id: 0.2,
                chance_attr2.id: 0.3,
                chance_attr3.id: 0.4},
            effects=(effect1_src1, effect2_src1, effect3_src1))
        self.mktype(
            src='src2',
            type_id=item_type_id,
            attrs={chance_attr1_id: 0.7},
            effects=(effect1_src2, effect2_src2))
        fit = Fit()
        item = Booster(item_type_id)
        fit.boosters.add(item)
        item.set_side_effect_status(effect1_id, True)
        item.set_side_effect_status(effect2_id, True)
        item.set_side_effect_status(effect3_id, True)
        # Action
        fit.source = 'src2'
        # Verification
        side_effects = item.side_effects
        self.assertEqual(len(side_effects), 1)
        self.assertIn(effect1_id, side_effects)
        side_effect1 = side_effects[effect1_id]
        self.assertIs(side_effect1.effect, effect1_src2)
        self.assertAlmostEqual(side_effect1.chance, 0.7)
        self.assertIs(side_effect1.status, True)
        # Action
        fit.source = 'src1'
        # Verification
        side_effects = item.side_effects
        self.assertEqual(len(side_effects), 3)
        self.assertIn(effect1_id, side_effects)
        side_effect1 = side_effects[effect1_id]
        self.assertIs(side_effect1.effect, effect1_src1)
        self.assertAlmostEqual(side_effect1.chance, 0.2)
        self.assertIs(side_effect1.status, True)
        self.assertIn(effect2_id, side_effects)
        side_effect2 = side_effects[effect2_id]
        self.assertIs(side_effect2.effect, effect2_src1)
        self.assertAlmostEqual(side_effect2.chance, 0.3)
        self.assertIs(side_effect2.status, True)
        self.assertIn(effect3_id, side_effects)
        side_effect3 = side_effects[effect3_id]
        self.assertIs(side_effect3.effect, effect3_src1)
        self.assertAlmostEqual(side_effect3.chance, 0.4)
        self.assertIs(side_effect3.status, True)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_enabling_attached(self):
        # Setup
        chance_attr = self.mkattr()
        src_attr = self.mkattr()
        tgt_attr = self.mkattr()
        modifier = self.mkmod(
            tgt_filter=ModTgtFilter.item,
            tgt_domain=ModDomain.self,
            tgt_attr_id=tgt_attr.id,
            operator=ModOperator.post_mul,
            src_attr_id=src_attr.id)
        effect = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr.id,
            modifiers=[modifier])
        fit = Fit()
        item = Booster(self.mktype(
            attrs={
                chance_attr.id: 0.5,
                tgt_attr.id: 100,
                src_attr.id: 1.2},
            effects=[effect]).id)
        fit.boosters.add(item)
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 100)
        # Action
        item.set_side_effect_status(effect.id, True)
        # Verification
        self.assertIs(item.side_effects[effect.id].status, True)
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 120)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_enabling_detached(self):
        # Setup
        chance_attr = self.mkattr()
        src_attr = self.mkattr()
        tgt_attr = self.mkattr()
        modifier = self.mkmod(
            tgt_filter=ModTgtFilter.item,
            tgt_domain=ModDomain.self,
            tgt_attr_id=tgt_attr.id,
            operator=ModOperator.post_mul,
            src_attr_id=src_attr.id)
        effect = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr.id,
            modifiers=[modifier])
        fit = Fit()
        item = Booster(self.mktype(
            attrs={
                chance_attr.id: 0.5,
                tgt_attr.id: 100,
                src_attr.id: 1.2},
            effects=[effect]).id)
        item.set_side_effect_status(effect.id, True)
        # Action
        fit.boosters.add(item)
        # Verification
        self.assertIs(item.side_effects[effect.id].status, True)
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 120)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_disabling_attached(self):
        # Setup
        chance_attr = self.mkattr()
        src_attr = self.mkattr()
        tgt_attr = self.mkattr()
        modifier = self.mkmod(
            tgt_filter=ModTgtFilter.item,
            tgt_domain=ModDomain.self,
            tgt_attr_id=tgt_attr.id,
            operator=ModOperator.post_mul,
            src_attr_id=src_attr.id)
        effect = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr.id,
            modifiers=[modifier])
        fit = Fit()
        item = Booster(self.mktype(
            attrs={
                chance_attr.id: 0.5,
                tgt_attr.id: 100,
                src_attr.id: 1.2},
            effects=[effect]).id)
        fit.boosters.add(item)
        item.set_side_effect_status(effect.id, True)
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 120)
        # Action
        item.set_side_effect_status(effect.id, False)
        # Verification
        self.assertIs(item.side_effects[effect.id].status, False)
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 100)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)

    def test_disabling_detached(self):
        # Setup
        chance_attr = self.mkattr()
        src_attr = self.mkattr()
        tgt_attr = self.mkattr()
        modifier = self.mkmod(
            tgt_filter=ModTgtFilter.item,
            tgt_domain=ModDomain.self,
            tgt_attr_id=tgt_attr.id,
            operator=ModOperator.post_mul,
            src_attr_id=src_attr.id)
        effect = self.mkeffect(
            category_id=EffectCategoryId.passive,
            fitting_usage_chance_attr_id=chance_attr.id,
            modifiers=[modifier])
        fit = Fit()
        item = Booster(self.mktype(
            attrs={
                chance_attr.id: 0.5,
                tgt_attr.id: 100,
                src_attr.id: 1.2},
            effects=[effect]).id)
        item.set_side_effect_status(effect.id, True)
        item.set_side_effect_status(effect.id, False)
        # Action
        fit.boosters.add(item)
        # Verification
        self.assertIs(item.side_effects[effect.id].status, False)
        self.assertAlmostEqual(item.attrs[tgt_attr.id], 100)
        # Cleanup
        self.assert_fit_buffers_empty(fit)
        self.assertEqual(len(self.get_log()), 0)
