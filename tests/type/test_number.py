# This Python file uses the following encoding: utf-8

from unittest import TestCase

from galactic.type.number import *


class ImpreciseFloatTest(TestCase):
    def test___init__(self):
        infinity = ImpreciseFloat()
        self.assertEqual(
            infinity.inf,
            -math.inf,
            "The lower limit of the real line is not correct"
        )
        self.assertEqual(
            infinity.sup,
            math.inf,
            "The upper limit of the real line is not correct"
        )
        lower_bounded = ImpreciseFloat(inf=0)
        self.assertEqual(
            lower_bounded.inf,
            0,
            "The lower limit of the positive numbers is not correct"
        )
        upper_bounded = ImpreciseFloat(sup=0)
        self.assertEqual(
            upper_bounded.sup,
            0,
            "The upper limit of the negative numbers is not correct"
        )
        contradiction = ImpreciseFloat(inf=5, sup=0)
        self.assertEqual(
            contradiction.inf,
            math.inf,
            "The lower limit of the contradiction is not correct"
        )
        self.assertEqual(
            contradiction.sup,
            -math.inf,
            "The upper limit of the contradiction is not correct"
        )

    def test___le__(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
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
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
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
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
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
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
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
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
        self.assertEqual(
            i_5_15 & i_5_10,
            ImpreciseFloat(inf=5, sup=10),
            "[5,15] & [5,10] = [5,10]"
        )
        self.assertEqual(
            i_5_15 & i_10_20,
            ImpreciseFloat(inf=10, sup=15),
            "[5,15] & [10,20] = [10,15]"
        )

    def test___or__(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
        self.assertEqual(
            i_5_15 | i_5_10,
            ImpreciseFloat(inf=5, sup=15),
            "[5,15] | [5,10] = [5,15]"
        )
        self.assertEqual(
            i_5_15 | i_10_20,
            ImpreciseFloat(inf=5, sup=20),
            "[5,15] | [10,20] = [5,20]"
        )

    def test__isdisjoint(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_15_20 = ImpreciseFloat(inf=15, sup=20)
        self.assertTrue(
            i_5_10.isdisjoint(i_15_20),
            "[5,10] is disjoint of [15,20]"
        )
        self.assertFalse(
            i_5_15.isdisjoint(i_15_20),
            "[5,15] is not disjoint of [15,20]"
        )

    def test_union(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
        self.assertEqual(
            i_5_15.union(i_5_10, i_10_20),
            ImpreciseFloat(inf=5, sup=20),
            "[5,15] | [5,10] | [10,20] = [5,20]"
        )

    def test_intersection(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        i_5_15 = ImpreciseFloat(inf=5, sup=15)
        i_10_20 = ImpreciseFloat(inf=10, sup=20)
        self.assertEqual(
            i_5_15.intersection(i_5_10, i_10_20),
            ImpreciseFloat(inf=10, sup=10),
            "[5,15] & [5,10] & [10,20] = [10,10]"
        )

    def test___repr__(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        self.assertEqual(
            repr(i_5_10),
            "ImpreciseFloat(inf=5.0, sup=10.0)",
            "[5,15] & [5,10] & [10,20] = [10,10]"
        )

    def test___str__(self):
        i_5_10 = ImpreciseFloat(inf=5, sup=10)
        print(i_5_10)
        self.assertEqual(
            str(i_5_10),
            "[5.0:10.0]",
            "str(ImpreciseFloat(inf=5, sup=10)) == [5.0:10.0]"
        )

