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


import logging

from tests.cache_generator.generator_testcase import GeneratorTestCase


class TestCleanupTypes(GeneratorTestCase):
    """
    Check which entries should stay in the data.
    """

    def test_group_character(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 1})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_group_effect_beacon(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 920})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_group_other(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 100.0% from evetypes')
        self.assertEqual(len(data['types']), 0)

    def test_group_character_unpublished(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 1, 'published': False})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_ship(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 6})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_module(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 7})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_charge(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 8})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_skill(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 16})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_drone(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 18})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_implant(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 20})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_subsystem(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 32})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_fighter(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 87})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 0.0% from evegroups, 0.0% from evetypes')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])

    def test_category_other(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 50})
        self.dh.data['evegroups'].append({'groupID': 50, 'categoryID': 51})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 100.0% from evegroups, 100.0% from evetypes')
        self.assertEqual(len(data['types']), 0)

    def test_mixed(self):
        self.dh.data['evetypes'].append({'typeID': 1, 'groupID': 920})
        self.dh.data['evetypes'].append({'typeID': 2, 'groupID': 50})
        self.dh.data['evetypes'].append({'typeID': 3, 'groupID': 20})
        self.dh.data['evegroups'].append({'groupID': 20, 'categoryID': 7})
        self.dh.data['evetypes'].append({'typeID': 4, 'groupID': 80})
        self.dh.data['evegroups'].append({'groupID': 80, 'categoryID': 700})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        idzing_stats = self.log[0]
        self.assertEqual(idzing_stats.name, 'eos.data.cache_generator.converter')
        self.assertEqual(idzing_stats.levelno, logging.WARNING)
        clean_stats = self.log[1]
        self.assertEqual(clean_stats.name, 'eos.data.cache_generator.cleaner')
        self.assertEqual(clean_stats.levelno, logging.INFO)
        self.assertEqual(clean_stats.msg, 'cleaned: 50.0% from evegroups, 50.0% from evetypes')
        self.assertEqual(len(data['types']), 2)
        self.assertIn(1, data['types'])
        self.assertIn(3, data['types'])
