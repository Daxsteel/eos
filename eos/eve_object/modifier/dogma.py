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


from numbers import Integral

from eos.const.eos import ModOperator
from eos.data.cachable import BaseCachable
from eos.util.repr import make_repr_str
from .base import BaseModifier
from .exception import ModificationCalculationError


class DogmaModifier(BaseModifier, BaseCachable):
    """Defines one of modifier types, dogma modifier.

    Dogma modifiers are the most typical modifier type. They always take
    attribute value which describes modification strength from item which
    carries modifier - it makes them less flexible, but they can be processed
    efficiently.
    """

    def __init__(
            self, tgt_filter=None, tgt_domain=None, tgt_filter_extra_arg=None,
            tgt_attr_id=None, operator=None, src_attr_id=None):
        BaseModifier.__init__(
            self, tgt_filter=tgt_filter, tgt_domain=tgt_domain,
            tgt_filter_extra_arg=tgt_filter_extra_arg, tgt_attr_id=tgt_attr_id)
        # Dogma modifier-specific attributes
        self.operator = operator
        self.src_attr_id = src_attr_id

    def get_modification(self, carrier_item, _):
        try:
            value = carrier_item.attrs[self.src_attr_id]
        # In case attribute value cannot be fetched, just raise error,
        # all error logging is handled in attribute container
        except KeyError as e:
            raise ModificationCalculationError from e
        else:
            return self.operator, value

    # Validation-related methods
    @property
    def _valid(self):
        return all((
            self._validate_base(),
            self.operator in ModOperator.__members__.values(),
            isinstance(self.src_attr_id, Integral)))

    # Cache-related methods
    def compress(self):
        return (
            self.tgt_filter,
            self.tgt_domain,
            self.tgt_filter_extra_arg,
            self.tgt_attr_id,
            self.operator,
            self.src_attr_id)

    @classmethod
    def decompress(cls, cache_handler, compressed):
        return cls(
            tgt_filter=compressed[0],
            tgt_domain=compressed[1],
            tgt_filter_extra_arg=compressed[2],
            tgt_attr_id=compressed[3],
            operator=compressed[4],
            src_attr_id=compressed[5])

    # Auxiliary methods
    def __repr__(self):
        return make_repr_str(self)
