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


from abc import ABCMeta, abstractmethod

from eos.util.repr import make_repr_str
from ..base import BaseStatRegister


class BaseResourceStatRegister(BaseStatRegister, metaclass=ABCMeta):

    @property
    @abstractmethod
    def used(self):
        ...

    @property
    @abstractmethod
    def output(self):
        ...

    @property
    @abstractmethod
    def _users(self):
        ...

    def __repr__(self):
        spec = ['used', 'output']
        return make_repr_str(self, spec)
