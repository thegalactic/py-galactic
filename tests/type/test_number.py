# This Python file uses the following encoding: utf-8

from unittest import TestCase

from galactic.type.number import *


class ImpreciseFloatTest(TestCase):
    def test___init__(self):
        infinity = ImpreciseFloat()
        self.assertEqual(
            infinity.lower,
            -math.inf,
            "The lower limit of the real line is not correct"
        )
        self.assertEqual(
            infinity.upper,
            math.inf,
            "The upper limit of the real line is not correct"
        )
        lower_bounded = ImpreciseFloat(lower=0)
        self.assertEqual(
            lower_bounded.lower,
            0,
            "The lower limit of the positive numbers is not correct"
        )
        upper_bounded = ImpreciseFloat(upper=0)
        self.assertEqual(
            upper_bounded.upper,
            0,
            "The upper limit of the negative numbers is not correct"
        )
        contradiction = ImpreciseFloat(lower=5, upper=0)
        self.assertEqual(
            contradiction.lower,
            math.inf,
            "The lower limit of the contradiction is not correct"
        )
        self.assertEqual(
            contradiction.upper,
            -math.inf,
            "The upper limit of the contradiction is not correct"
        )

    def test___le__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertTrue(
            i_5_10.issubset(i_5_15),
            "[5,10] <= [5,15]"
        )
        self.assertTrue(
            i_5_10.issubset(i_5_10),
            "[5,10] <= [5,10]"
        )
        self.assertFalse(
            i_5_10.issubset(i_10_20),
            "not [5,10] <= [10,20]"
        )

    def test___lt__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertTrue(
            i_5_10 < i_5_15,
            "[5,10] < [5,15]"
        )
        self.assertFalse(
            i_5_10 < i_5_10,
            "not [5,10] < [5,10]"
        )
        self.assertFalse(
            i_5_10 < i_10_20,
            "not [5,10] < [10,20]"
        )

    def test___ge__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertTrue(
            i_5_15.issuperset(i_5_10),
            "[5,15] >= [5,10]"
        )
        self.assertTrue(
            i_5_10.issuperset(i_5_10),
            "[5,10] >= [5,10]"
        )
        self.assertFalse(
            i_5_10.issuperset(i_10_20),
            "not [5,10] >= [10,20]"
        )

    def test___gt__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertTrue(
            i_5_15 > i_5_10,
            "[5,15] > [5,10]"
        )
        self.assertFalse(
            i_5_10 > i_5_10,
            "not [5,10] > [5,10]"
        )
        self.assertFalse(
            i_5_10 > i_10_20,
            "not [5,10] > [10,20]"
        )

    def test___and__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertEqual(
            i_5_15 & i_5_10,
            ImpreciseFloat(lower=5, upper=10),
            "[5,15] & [5,10] = [5,10]"
        )
        self.assertEqual(
            i_5_15 & i_10_20,
            ImpreciseFloat(lower=10, upper=15),
            "[5,15] & [10,20] = [10,15]"
        )

    def test___or__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertEqual(
            i_5_15 | i_5_10,
            ImpreciseFloat(lower=5, upper=15),
            "[5,15] | [5,10] = [5,15]"
        )
        self.assertEqual(
            i_5_15 | i_10_20,
            ImpreciseFloat(lower=5, upper=20),
            "[5,15] | [10,20] = [5,20]"
        )

    def test__isdisjoint(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_15_20 = ImpreciseFloat(lower=15, upper=20)
        self.assertTrue(
            i_5_10.isdisjoint(i_15_20),
            "[5,10] is disjoint of [15,20]"
        )
        self.assertFalse(
            i_5_15.isdisjoint(i_15_20),
            "[5,15] is not disjoint of [15,20]"
        )

    def test_union(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertEqual(
            i_5_15.union(i_5_10, i_10_20),
            ImpreciseFloat(lower=5, upper=20),
            "[5,15] | [5,10] | [10,20] = [5,20]"
        )

    def test_intersection(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        i_5_15 = ImpreciseFloat(lower=5, upper=15)
        i_10_20 = ImpreciseFloat(lower=10, upper=20)
        self.assertEqual(
            i_5_15.intersection(i_5_10, i_10_20),
            ImpreciseFloat(lower=10, upper=10),
            "[5,15] & [5,10] & [10,20] = [10,10]"
        )

    def test___repr__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        self.assertEqual(
            repr(i_5_10),
            "ImpreciseFloat(lower=5.0, upper=10.0)",
            "[5,15] & [5,10] & [10,20] = [10,10]"
        )

    def test___str__(self):
        i_5_10 = ImpreciseFloat(lower=5, upper=10)
        print(i_5_10)
        self.assertEqual(
            str(i_5_10),
            "[5.0:10.0]",
            "str(ImpreciseFloat(lower=5, upper=10)) == [5.0:10.0]"
        )

class ImpreciseIntegerTest(TestCase):
    def test___init__(self):
        infinity = ImpreciseInteger()
        self.assertEqual(
            infinity.lower,
            -sys.maxsize,
            "The lower limit of the real line is not correct"
        )
        self.assertEqual(
            infinity.upper,
            sys.maxsize,
            "The upper limit of the real line is not correct"
        )
        lower_bounded = ImpreciseInteger(lower=0)
        self.assertEqual(
            lower_bounded.lower,
            0,
            "The lower limit of the positive numbers is not correct"
        )
        upper_bounded = ImpreciseInteger(upper=0)
        self.assertEqual(
            upper_bounded.upper,
            0,
            "The upper limit of the negative numbers is not correct"
        )
        contradiction = ImpreciseInteger(lower=5, upper=0)
        self.assertEqual(
            contradiction.lower,
            sys.maxsize,
            "The lower limit of the contradiction is not correct"
        )
        self.assertEqual(
            contradiction.upper,
            -sys.maxsize,
            "The upper limit of the contradiction is not correct"
        )
