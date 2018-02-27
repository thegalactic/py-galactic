# This Python file uses the following encoding: utf-8

from unittest import TestCase

from galactic.type.category import *


class ImpreciseCategoryTest(TestCase):
    def test_imprecise_category(self):
        Null = imprecise_category('Null')
        self.assertEqual(
            str(Null),
            "test_category.Null",
            "The string representation of the class is not correct"
        )
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        self.assertEqual(
            str(Color),
            "test_category.Color",
            "The string representation of the class is not correct"
        )
        Color = imprecise_category('Color', ['R', 'G', 'B'], module='mymodule')
        self.assertEqual(
            str(Color),
            "mymodule.Color",
            "The string representation of the class is not correct"
        )

    def test___new__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        self.assertEqual(
            str(Color()),
            "{}",
            "The string representation of an empty category is not correct"
        )
        self.assertEqual(
            str(Color(['R', 'G'])),
            "{'R', 'G'}",
            "The string representation of a non-empty category is not correct"
        )
        self.assertFalse(
            Color(['R', 'G']) is Color(['R', 'G']),
            "The instances must not be identical"
        )
        Color = imprecise_category('Color', ['R', 'G', 'B'], cache=True)
        self.assertTrue(
            Color(['R', 'G']) is Color(['R', 'G']),
            "The instances must be identical"
        )

    def test___contains__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color = Color(['R', 'G'])
        self.assertTrue(
            'G' in color,
            "G belongs to the color"
        )
        self.assertFalse(
            'B' in color,
            "B does not belong to the color"
        )
        with self.assertRaises(ValueError):
            _ = 'X' in color

    def test___len__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color = Color(['R', 'G'])
        self.assertEqual(
            len(color),
            2,
            "The length of the color must be 2"
        )

    def test___iter__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color = Color(['R', 'G'])
        self.assertEqual(
            [item for item in color],
            ['R', 'G'],
            "The iteration over the color must be ['R', 'G']"
        )

    def test___le__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['R'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertTrue(
            color1 <= color2,
            "['R'] is a subset of ['R', 'G']"
        )
        self.assertTrue(
            color1 <= color1,
            "['R'] is a subset of ['R']"
        )
        self.assertFalse(
            color2 <= color3,
            "['R', 'G'] is not a subset of ['R', 'B']"
        )
        with self.assertRaises(TypeError):
            _ = color1 <= 'dummy'

    def test___lt__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['R'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertTrue(
            color1 < color2,
            "['R'] is a strict subset of ['R', 'G']"
        )
        self.assertFalse(
            color1 < color1,
            "['R'] is not a strict subset of ['R']"
        )
        self.assertFalse(
            color2 < color3,
            "['R', 'G'] is not a strict subset of ['R', 'B']"
        )
        with self.assertRaises(TypeError):
            _ = color1 < 'dummy'

    def test___eq__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['R'])
        color2 = Color(['R', 'G'])
        self.assertFalse(
            color1 == color2,
            "['R'] is not equal to ['R', 'G']"
        )
        self.assertTrue(
            color1 == color1,
            "['R'] is equal to ['R']"
        )
        with self.assertRaises(TypeError):
            _ = color1 == 'dummy'

    def test___gt__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['R'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertTrue(
            color2 > color1,
            "['R', 'G'] is a strict superset of ['R']"
        )
        self.assertFalse(
            color1 > color1,
            "['R'] is not a strict superset of ['R']"
        )
        self.assertFalse(
            color2 > color3,
            "['R', 'G'] is not a strict superset of ['R', 'B']"
        )
        with self.assertRaises(TypeError):
            _ = color1 > 'dummy'

    def test___and__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['R'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertEqual(
            color1,
            color2 & color3,
            "['R', 'G'] & ['R', 'B'] = ['R']"
        )
        with self.assertRaises(TypeError):
            _ = color1 & 'dummy'

    def test___or__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['R', 'G', 'B'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertEqual(
            color1,
            color2 | color3,
            "['R', 'G'] | ['R', 'B'] = ['R', 'G', 'B']"
        )
        with self.assertRaises(TypeError):
            _ = color1 | 'dummy'

    def test___sub__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['G'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertEqual(
            color1,
            color2 - color3,
            "['R', 'G'] - ['R', 'B'] = ['B']"
        )
        with self.assertRaises(TypeError):
            _ = color1 - 'dummy'

    def test___xor__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['G', 'B'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertEqual(
            color1,
            color2 ^ color3,
            "['R', 'G'] - ['R', 'B'] = ['G', 'B']"
        )
        with self.assertRaises(TypeError):
            _ = color1 ^ 'dummy'

    def test_isdisjoint(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['B'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertTrue(
            color1.isdisjoint(color2),
            "bool(['B'] & ['R', 'G']) = True"
        )
        self.assertFalse(
            color1.isdisjoint(color3),
            "bool(['B'] & ['R', 'B']) = False"
        )
        self.assertTrue(
            color1.isdisjoint(['R', 'G']),
            "bool(['B'] & ['R', 'G']) = True"
        )
        with self.assertRaises(TypeError):
            _ = color1.isdisjoint(125)

    def test_issubset(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['B'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertFalse(
            color1.issubset(color2),
            "['B'] is not a subset of ['R', 'G']"
        )
        self.assertTrue(
            color1.issubset(color3),
            "['B'] is a subset of ['R', 'B']"
        )
        self.assertTrue(
            color1.issubset(['B', 'G']),
            "['B'] is a subset of ['B', 'G']"
        )
        with self.assertRaises(TypeError):
            _ = color1.issubset(125)

    def test_issuperset(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['B'])
        color2 = Color(['R', 'G'])
        color3 = Color(['R', 'B'])
        self.assertFalse(
            color1.issuperset(color2),
            "['B'] is not a superset of ['R', 'G']"
        )
        self.assertTrue(
            color3.issuperset(color1),
            "['R', 'B'] is a superset of ['B']"
        )
        self.assertTrue(
            color3.issuperset(['R']),
            "['R', 'B'] is a superset of ['R']"
        )
        with self.assertRaises(TypeError):
            _ = color1.issuperset(125)

    def test_union(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['B', 'R'])
        color2 = Color()
        color3 = Color(['B'])
        self.assertEqual(
            color3.union(color2, ['R']),
            color1,
            "['B'] | [] | ['R'] =  ['B', 'R']"
        )

    def test_intersection(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['B'])
        color2 = Color(['B', 'R'])
        color3 = Color(['R', 'G', 'B'])
        self.assertEqual(
            color3.intersection(color2, ['B']),
            color1,
            "['R', 'G', 'B'] & ['B', 'R'] & ['B'] =  ['B']"
        )

    def test_difference(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['G'])
        color2 = Color(['B', 'R'])
        color3 = Color(['R', 'G', 'B'])
        self.assertEqual(
            color3.difference(color2, ['B']),
            color1,
            "['R', 'G', 'B'] - ['B', 'R'] - ['B'] =  ['G']"
        )

    def test_symmetric_difference(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color1 = Color(['B', 'G'])
        color2 = Color(['B', 'R'])
        color3 = Color(['R', 'G'])
        self.assertEqual(
            color3.symmetric_difference(color2),
            color1,
            "['R', 'G'] ^ ['B', 'R'] = ['B', 'G']"
        )
        self.assertEqual(
            color3.symmetric_difference(['B', 'G']),
            Color(['R', 'B']),
            "['R', 'G'] ^ ['B', 'G'] = ['B', 'R]"
        )
        with self.assertRaises(TypeError):
            _ = color1.symmetric_difference(125)

    def test___repr__(self):
        Color = imprecise_category('Color', ['R', 'G', 'B'])
        color = Color(['B', 'G'])
        self.assertEqual(
            repr(color),
            "Color({'G', 'B'})",
            "repr(Color(['B', 'G'])) = Color({'G', 'B'})"
        )

class CategoryTest(TestCase):
    def test_category(self):
        Color = category('Color', ['R', 'G', 'B'])
        self.assertEqual(
            str(Color),
            "<class 'test_category.Color'>",
            "The string representation of the class is not correct"
        )
        Color = category('Color', ['R', 'G', 'B'], module='mymodule')
        self.assertEqual(
            str(Color),
            "<class 'mymodule.Color'>",
            "The string representation of the class is not correct"
        )
        with self.assertRaises(ValueError):
            _ = category('Color')

    def test___new__(self):
        Color = category('Color', ['R', 'G', 'B'])
        self.assertEqual(
            str(Color()),
            "R",
            "The string representation of the instance is not correct"
        )
        self.assertEqual(
            str(Color('B')),
            "B",
            "The string representation of the instance is not correct"
        )
        with self.assertRaises(ValueError):
            _ = Color('Y')

    def test___repr__(self):
        Color = category('Color', ['R', 'G', 'B'])
        self.assertEqual(
            repr(Color()),
            "Color('R')",
            "The representation of the instance is not correct"
        )
