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


from copy import deepcopy
from logging import getLogger, DEBUG
from logging.handlers import BufferingHandler
from unittest import TestCase
from unittest.mock import DEFAULT

from .environment import CacheHandler


class TestLogHandler(BufferingHandler):
    """
    Custom logging handler class which helps to
    check log output without unnecessary actual
    output.
    """
    def __init__(self):
        # Capacity is zero, as we won't rely on
        # it when deciding when to flush data
        BufferingHandler.__init__(self, 0)

    def shouldFlush(self, *args):
        return False

    def emit(self, record):
        self.buffer.append(record)


class EosTestCase(TestCase):
    """
    Custom test case class, which incorporates several environment
    changes for ease of test process, namely:

    self.log -- access to output generated by logging
        facility during test
    self.ch -- default cache handler
    self.assert_object_buffers_empty -- checks if buffers (attributes
        which have length) of passed object are clear

    When overriding setUp and tearDown methods, make sure
    to call this class' methods (before anything else is
    done for setUp, and after for tearDown).
    """

    def setUp(self):
        logger = getLogger()
        # Save existing data about logging system (log level and handlers)
        self.__old_loglevel = logger.getEffectiveLevel()
        logger.setLevel(DEBUG)
        self.__removed_log_handlers = []
        for handler in logger.handlers:
            self.__removed_log_handlers.append(handler)
            logger.removeHandler(handler)
        # Place test logger instead of them
        self.__test_log_handler = TestLogHandler()
        logger.addHandler(self.__test_log_handler)
        # Add cache handler to each test case
        self.ch = CacheHandler()

    def tearDown(self):
        # Remove test logger and restore loggers which
        # were removed during setup
        logger = getLogger()
        logger.removeHandler(self.__test_log_handler)
        self.__test_log_handler.close()
        for handler in self.__removed_log_handlers:
            logger.addHandler(handler)
        logger.setLevel(self.__old_loglevel)

    @property
    def log(self):
        return self.__test_log_handler.buffer

    def assert_object_buffers_empty(self, object_, ignore=()):
        entry_num = self._get_object_buffer_entry_amount(object_, ignore=ignore)
        # Raise error if we found any data in any attached storage
        if entry_num > 0:
            plu = 'y' if entry_num == 1 else 'ies'
            msg = '{} entr{} in buffers: buffers must be empty'.format(entry_num, plu)
            self.fail(msg=msg)

    def _get_object_buffer_entry_amount(self, object_, ignore=()):
        """
        Returns amount of entries stored on this instance,
        useful to detect memory leaks.
        """
        entry_num = 0
        for attr_name, attr_val in object_.__dict__.items():
            if attr_name in ignore:
                continue
            attr_val = getattr(object_, attr_name)
            # Ignore strings, as Eos doesn't deal with them -
            # they are mostly used to refer various attributes
            # and are stored on object permanently
            if isinstance(attr_val, str):
                continue
            try:
                attr_len = len(attr_val)
            except TypeError:
                pass
            else:
                entry_num += attr_len
        return entry_num

    def _setup_args_capture(self, mock_obj, arg_list):
        """
        In case when we want to capture exact state of arguments passed
        to mock (to verify what they looked like, if they were further
        modified by object under test), we have to copy them at the time
        they were passed to mock. This method assists with this, it takes
        passed mock and records copies of all passed arguments into list
        passed as second argument in the form of tuple (args, kwargs}.
        """

        def capture_args(*args, **kwargs):
            arg_list.append((deepcopy(args), deepcopy(kwargs)))
            return DEFAULT

        mock_obj.side_effect = capture_args
