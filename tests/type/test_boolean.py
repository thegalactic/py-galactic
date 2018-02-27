# This Python file uses the following encoding: utf-8

from unittest import TestCase

from galactic.type.boolean import *


class ImpreciseBooleanTest(TestCase):
    def test___new__(self):
        boolean = ImpreciseBoolean([True, False])
        self.assertEqual(
            str(boolean),
            "{True, False}",
            "The string representation of an imprecise boolean is not correct"
        )
