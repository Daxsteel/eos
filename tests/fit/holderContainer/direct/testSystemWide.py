#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
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
#===============================================================================


from unittest.mock import Mock

from eos.const.eos import State
from eos.tests.fit.fitTestCase import FitTestCase


class TestDirectHolderSystemWide(FitTestCase):

    def _customMembershipCheck(self, fit, holder):
        self.assertIs(fit.systemWide, holder)

    def testDetachedNoneToNone(self):
        fit = self._makeFit()
        # Action
        fit.systemWide = None
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertIsNone(fit.systemWide)
        # Misc
        self.assertFitBuffersEmpty(fit)

    def testDetachedNoneToHolder(self):
        fit = self._makeFit()
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        # Action
        fit.systemWide = holder
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertIs(fit.systemWide, holder)
        self.assertIs(holder._fit, fit)
        # Misc
        fit.systemWide = None
        self.assertFitBuffersEmpty(fit)

    def testDetachedNoneToHolderFailure(self):
        fit = self._makeFit()
        fitOther = self._makeFit()
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fitOther.systemWide = holder
        # Action
        self.assertRaises(ValueError, fit.__setattr__, 'systemWide', holder)
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertEqual(len(fitOther.lt), 0)
        self.assertEqual(len(fitOther.rt), 0)
        self.assertIsNone(fit.systemWide)
        self.assertIs(fitOther.systemWide, holder)
        self.assertIs(holder._fit, fitOther)
        # Misc
        fitOther.systemWide = None
        self.assertFitBuffersEmpty(fit)
        self.assertFitBuffersEmpty(fitOther)

    def testDetachedHolderToHolder(self):
        fit = self._makeFit()
        holder1 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        holder2 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit.systemWide = holder1
        # Action
        fit.systemWide = holder2
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertIs(fit.systemWide, holder2)
        self.assertIsNone(holder1._fit)
        self.assertIs(holder2._fit, fit)
        # Misc
        fit.systemWide = None
        self.assertFitBuffersEmpty(fit)

    def testDetachedHolderToHolderFailure(self):
        fit = self._makeFit()
        fitOther = self._makeFit()
        holder1 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        holder2 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit.systemWide = holder1
        fitOther.systemWide = holder2
        # Action
        self.assertRaises(ValueError, fit.__setattr__, 'systemWide', holder2)
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertEqual(len(fitOther.lt), 0)
        self.assertEqual(len(fitOther.rt), 0)
        self.assertIs(fit.systemWide, holder1)
        self.assertIs(fitOther.systemWide, holder2)
        self.assertIs(holder1._fit, fit)
        self.assertIs(holder2._fit, fitOther)
        # Misc
        fit.systemWide = None
        fitOther.systemWide = None
        self.assertFitBuffersEmpty(fit)
        self.assertFitBuffersEmpty(fitOther)

    def testDetachedHolderToNone(self):
        fit = self._makeFit()
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit.systemWide = holder
        # Action
        fit.systemWide = None
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertIsNone(fit.systemWide)
        self.assertIsNone(holder._fit)
        # Misc
        self.assertFitBuffersEmpty(fit)

    def testAttachedNoneToNone(self):
        eos = Mock(spec_set=())
        fit = self._makeFit(eos=eos)
        # Action
        fit.systemWide = None
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertIsNone(fit.systemWide)
        # Misc
        self.assertFitBuffersEmpty(fit)

    def testAttachedNoneToHolder(self):
        eos = Mock(spec_set=())
        fit = self._makeFit(eos=eos)
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        # Action
        fit.systemWide = holder
        # Checks
        self.assertEqual(len(fit.lt), 1)
        self.assertIn(holder, fit.lt)
        self.assertEqual(fit.lt[holder], {State.offline, State.online, State.active})
        self.assertEqual(len(fit.rt), 1)
        self.assertIn(holder, fit.rt)
        self.assertEqual(fit.rt[holder], {State.offline, State.online, State.active})
        self.assertIs(fit.systemWide, holder)
        self.assertIs(holder._fit, fit)
        # Misc
        fit.systemWide = None
        self.assertFitBuffersEmpty(fit)

    def testAttachedNoneToHolderFailure(self):
        eos = Mock(spec_set=())
        fit = self._makeFit(eos=eos)
        fitOther = self._makeFit(eos=eos)
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fitOther.systemWide = holder
        # Action
        self.assertRaises(ValueError, fit.__setattr__, 'systemWide', holder)
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertEqual(len(fitOther.lt), 1)
        self.assertIn(holder, fitOther.lt)
        self.assertEqual(fitOther.lt[holder], {State.offline, State.online, State.active})
        self.assertEqual(len(fitOther.rt), 1)
        self.assertIn(holder, fitOther.rt)
        self.assertEqual(fitOther.rt[holder], {State.offline, State.online, State.active})
        self.assertIsNone(fit.systemWide)
        self.assertIs(fitOther.systemWide, holder)
        self.assertIs(holder._fit, fitOther)
        # Misc
        fitOther.systemWide = None
        self.assertFitBuffersEmpty(fit)
        self.assertFitBuffersEmpty(fitOther)

    def testAttachedHolderToHolder(self):
        eos = Mock(spec_set=())
        fit = self._makeFit(eos=eos)
        holder1 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        holder2 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit.systemWide = holder1
        # Action
        fit.systemWide = holder2
        # Checks
        self.assertEqual(len(fit.lt), 1)
        self.assertIn(holder2, fit.lt)
        self.assertEqual(fit.lt[holder2], {State.offline, State.online, State.active})
        self.assertEqual(len(fit.rt), 1)
        self.assertIn(holder2, fit.rt)
        self.assertEqual(fit.rt[holder2], {State.offline, State.online, State.active})
        self.assertIs(fit.systemWide, holder2)
        self.assertIsNone(holder1._fit)
        self.assertIs(holder2._fit, fit)
        # Misc
        fit.systemWide = None
        self.assertFitBuffersEmpty(fit)

    def testAttachedHolderToHolderFailure(self):
        eos = Mock(spec_set=())
        fit = self._makeFit(eos=eos)
        fitOther = self._makeFit(eos=eos)
        holder1 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        holder2 = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit.systemWide = holder1
        fitOther.systemWide = holder2
        # Action
        self.assertRaises(ValueError, fit.__setattr__, 'systemWide', holder2)
        # Checks
        self.assertEqual(len(fit.lt), 1)
        self.assertIn(holder1, fit.lt)
        self.assertEqual(fit.lt[holder1], {State.offline, State.online, State.active})
        self.assertEqual(len(fit.rt), 1)
        self.assertIn(holder1, fit.rt)
        self.assertEqual(fit.rt[holder1], {State.offline, State.online, State.active})
        self.assertEqual(len(fitOther.lt), 1)
        self.assertIn(holder2, fitOther.lt)
        self.assertEqual(fitOther.lt[holder2], {State.offline, State.online, State.active})
        self.assertEqual(len(fitOther.rt), 1)
        self.assertIn(holder2, fitOther.rt)
        self.assertEqual(fitOther.rt[holder2], {State.offline, State.online, State.active})
        self.assertIs(fit.systemWide, holder1)
        self.assertIs(fitOther.systemWide, holder2)
        self.assertIs(holder1._fit, fit)
        self.assertIs(holder2._fit, fitOther)
        # Misc
        fit.systemWide = None
        fitOther.systemWide = None
        self.assertFitBuffersEmpty(fit)
        self.assertFitBuffersEmpty(fitOther)

    def testAttachedHolderToNone(self):
        eos = Mock(spec_set=())
        fit = self._makeFit(eos=eos)
        holder = Mock(_fit=None, state=State.active, spec_set=('_fit', 'state'))
        fit.systemWide = holder
        # Action
        fit.systemWide = None
        # Checks
        self.assertEqual(len(fit.lt), 0)
        self.assertEqual(len(fit.rt), 0)
        self.assertIsNone(fit.systemWide)
        self.assertIsNone(holder._fit)
        # Misc
        self.assertFitBuffersEmpty(fit)
