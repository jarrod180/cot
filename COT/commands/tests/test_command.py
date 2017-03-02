#!/usr/bin/env python
#
# test_command.py - test cases for the generic ReadWriteCommand class
#
# January 2015, Glenn F. Matthews
# Copyright (c) 2015-2017 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.

"""Test cases for COT.commands.ReadWriteCommand class."""

from COT.tests.ut import COT_UT
from COT.ui import UI
from COT.commands import ReadWriteCommand
from COT.vm_description import VMInitError


class TestReadWriteCommand(COT_UT):
    """Test cases for ReadWriteCommand class."""

    def setUp(self):
        """Test case setup function called automatically prior to each test."""
        super(TestReadWriteCommand, self).setUp()
        self.instance = ReadWriteCommand(UI())
        self.instance.output = self.temp_file

    def test_vmfactory_fail(self):
        """If package/output are unsupported, expect a VMInitError."""
        self.instance.output = "foo.vmx"
        with self.assertRaises(VMInitError):
            self.instance.package = self.input_ovf

    def test_create_subparser_noop(self):
        """The generic class doesn't create a subparser."""
        self.instance.create_subparser()

    def test_set_output_implicitly(self):
        """If 'output' is not specifically set, run() sets it to 'package'."""
        self.instance = ReadWriteCommand(UI())
        self.instance.package = self.input_ovf
        self.assertEqual(self.instance.output, "")
        self.instance.run()
        self.assertEqual(self.instance.output, self.input_ovf)