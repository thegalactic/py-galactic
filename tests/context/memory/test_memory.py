# This Python file uses the following encoding: utf-8

from unittest import TestCase

from galactic.context.memory import *


class MemoryContextTest(TestCase):
    def test___init__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            str(context),
            "{'population': [], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}",
            "The context has not been correctly initialized"
        )
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            str(context.population),
            "['0', '1']",
            "The context has not been correctly initialized"
        )
        self.assertEqual(
            str(context.model),
            "{'mybool': <class 'bool'>, 'myint': <class 'int'>}",
            "The context has not been correctly initialized"
        )
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals={'0': {'mybool': True}, '1': {'myint': 1}}
        )
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': True, 'myint': 0}",
            "The context has not been correctly initialized"
        )
        self.assertEqual(
            str(context.population['1']),
            "{'mybool': False, 'myint': 1}",
            "The context has not been correctly initialized"
        )
        with self.assertRaises(TypeError):
            _ = MemoryContext(definition='bad value')
        with self.assertRaises(TypeError):
            _ = MemoryContext(individuals=1000)

    def test_population(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertTrue(
            isinstance(context.population, Population),
            "The property population is instance of Population"
        )

    def test_model(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertTrue(
            isinstance(context.model, Model),
            "The property model is instance of Model"
        )

    def test___contains__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertTrue(
            context.population['0'] in context,
            "The first individual of the context is in the context"
        )
        self.assertTrue(
            context.model['mybool'] in context,
            "The first attribute of the context is in the context"
        )
        other = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertFalse(
            other.population['0'] in context,
            "An unknown element is not in the context"
        )

    def test___bool__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertTrue(
            context,
            "The context is not empty"
        )
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertFalse(
            context,
            "The context is empty"
        )
        context = MemoryContext(
            individuals=['0', '1']
        )
        self.assertFalse(
            context,
            "The context is empty"
        )

    def test___str__(self):
        context = MemoryContext(
            definition={'mybool': bool},
            individuals=['0']
        )
        self.assertEqual(
            str(context),
            "{'population': ['0'], 'model': {'mybool': <class 'bool'>}}",
            "The string representation of this context is not correct"
        )


class MemoryPopulationTest(TestCase):
    def test_context(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            context.population.context,
            context,
            "The context of the population must be the original context"
        )

    def test_model(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            context.population.model,
            context.model,
            "The model of the population must be the original model"
        )

    def test___getitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': False, 'myint': 0}",
            "The textual representation of the first individual is not correct"
        )

    def test___setitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        context.population['0'] = {}
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': False, 'myint': 0}",
            "The population is not correct"
        )
        context.population['0'] = {'mybool': True}
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': True, 'myint': 0}",
            "The population is not correct"
        )
        with self.assertRaises(KeyError):
            context.population['0'] = {'abc': 1}

    def test___delitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        del context.population['0']
        self.assertFalse(
            bool(context.population),
            "The population must be empty"
        )

    def test___len__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            len(context.population),
            2,
            "The length of the population is not correct"
        )

    def test___bool__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertFalse(
            bool(context.population),
            "The population must be empty"
        )
        context.population['0'] = {}
        self.assertTrue(
            bool(context.population),
            "The population must be not empty"
        )

    def test___iter__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        for identifier, individual in context.population.items():
            self.assertTrue(
                isinstance(individual, Individual),
                "Each individual must be an instance of the Individual class"
            )
            self.assertTrue(
                isinstance(identifier, str),
                "Each identifier must be a str"
            )

    def test___str__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            str(context.population),
            "['0', '1']",
            "The string representation of the population is not correct"
        )


class MemoryModelTest(TestCase):
    def test_context(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            context.model.context,
            context,
            "The context of the model must be the original context"
        )

    def test_population(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            context.model.population,
            context.population,
            "The population of the model must be the original population"
        )

    def test___getitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            str(context.model['mybool']),
            "{'name': 'mybool', 'type': <class 'bool'>}",
            "The attribute mybool is not correct"
        )

    def test___setitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals={'0': {'mybool': True}, '1': {'myint': 1}}
        )
        context.model['mybool'] = bool
        self.assertEqual(
            {identifier: str(individual) for identifier, individual in context.population.items()},
            {'0': "{'mybool': True, 'myint': 0}", '1': "{'mybool': False, 'myint': 1}"},
            "The individuals must remain unchanged"
        )
        context.model['mybool'] = int
        self.assertEqual(
            {identifier: str(individual) for identifier, individual in context.population.items()},
            {'0': "{'mybool': 1, 'myint': 0}", '1': "{'mybool': 0, 'myint': 1}"},
            "The individuals must change"
        )
        context.model['mybool'] = list
        self.assertEqual(
            {identifier: str(individual) for identifier, individual in context.population.items()},
            {'0': "{'mybool': [], 'myint': 0}", '1': "{'mybool': [], 'myint': 1}"},
            "The individuals must change"
        )
        del context.model['myint']
        context.model['myint2'] = int
        self.assertEqual(
            {identifier: str(individual) for identifier, individual in context.population.items()},
            {'0': "{'mybool': [], 'myint2': 0}", '1': "{'mybool': [], 'myint2': 0}"},
            "The individuals must change"
        )

    def test___delitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        del context.model['mybool']
        self.assertEqual(
            str(context),
            "{'population': ['0', '1'], 'model': {'myint': <class 'int'>}}",
            "The context is not correct"
        )
        self.assertEqual(
            str(context.population['0']),
            "{'myint': 0}",
            "The context is not correct"
        )

    def test___len__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            len(context.model),
            2,
            "The length of the model is not correct"
        )

    def test___bool__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertTrue(
            bool(context.model),
            "The bool representation of the model is not correct"
        )

    def test___iter__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            list(iter(context.model)),
            ['mybool', 'myint'],
            "The iteration over the model is not correct"
        )

    def test___str__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int}
        )
        self.assertEqual(
            str(context.model),
            "{'mybool': <class 'bool'>, 'myint': <class 'int'>}",
            "The string representation of the model must be correct"
        )


class MemoryIndividualTest(TestCase):
    def test_identifier(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.population['0'].identifier,
            '0',
            "The identifier must be '0'"
        )

    def test_population(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.population['0'].population,
            context.population,
            "The population of the individual named '0' must be the context population"
        )

    def test_context(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.population['0'].context,
            context,
            "The context of the individual named '0' must be the context"
        )

    def test_model(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.population['0'].model,
            context.model,
            "The model of the individual named '0' must be the context model"
        )

    def test_value(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.population['0'].value(context.model['mybool']),
            bool(),
            "The value 'mybool' of the individual named '0' must be the False"
        )
        self.assertEqual(
            context.population['0'].value(context.model['myint']),
            int(),
            "The value 'myint' of the individual named '0' must be the 0"
        )
        other = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        with self.assertRaises(ValueError):
            _ = context.population['0'].value(other.model['myint'])

    def test___setitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        context.population['0']['mybool'] = True
        context.population['0']['myint'] = 1
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': True, 'myint': 1}",
            "The textual representation of the first individual is not correct"
        )
        context.population['1']['mybool'] = True
        context.population['1']['myint'] = 2
        self.assertEqual(
            str(context.population['1']),
            "{'mybool': True, 'myint': 2}",
            "The textual representation of the first individual is not correct"
        )
        with self.assertRaises(KeyError):
            context.population['0']['unknown'] = 1
        with self.assertRaises(ValueError):
            context.population['0']['myint'] = 'abc'

    def test___getitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.population['0']['mybool'],
            bool(),
            "The first value is not correct"
        )
        self.assertEqual(
            context.population['0']['myint'],
            int(),
            "The second value is not correct"
        )
        with self.assertRaises(KeyError):
            _ = context.population['0']['unknown']

    def test___delitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        with self.assertRaises(ValueError):
            del context.population['0']['myint']

    def test___len__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            len(context.population['0']),
            2,
            "The length of the individual is not correct"
        )

    def test___eq__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertTrue(
            context.population['0'] == context.population['0'],
            "The individual is equal to itself"
        )
        self.assertFalse(
            context.population['0'] == context.population['1'],
            "Two different individuals are unequal"
        )
        other = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertFalse(
            context.population['0'] == other.population['0'],
            "Two individuals from two different contexts are unequal"
        )

    def test___iter__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            list(iter(context.population['0'])),
            ['mybool', 'myint'],
            "The iteration over the individual is not correct"
        )

    def test___str__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': False, 'myint': 0}",
            "The string representation of the individual is not correct"
        )


class MemoryAttributeTest(TestCase):
    def test_name(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.model['mybool'].name,
            'mybool',
            "The name must be 'mybool'"
        )

    def test_type(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0']
        )
        self.assertEqual(
            context.model['mybool'].type,
            bool,
            "The type must be bool"
        )

    def test_value(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            context.model['mybool'].value(context.population['0']),
            context.population['0'].value(context.model['mybool']),
            "The value must be correct"
        )

    def test___getitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            context.model['mybool']['0'],
            context.population['0']['mybool'],
            "The value must be correct"
        )

    def test___setitem__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        context.model['mybool']['0'] = True
        context.model['myint']['0'] = 1
        self.assertEqual(
            str(context.population['0']),
            "{'mybool': True, 'myint': 1}",
            "The textual representation of the first individual is not correct"
        )
        context.model['mybool']['1'] = True
        context.model['myint']['1'] = 2
        self.assertEqual(
            str(context.population['1']),
            "{'mybool': True, 'myint': 2}",
            "The textual representation of the first individual is not correct"
        )
        with self.assertRaises(KeyError):
            context.model['mybool']['unknown'] = 1
        with self.assertRaises(ValueError):
            context.model['myint']['0'] = 'abc'

    def test___len__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            len(context.model['mybool']),
            2,
            "The length must be correct"
        )

    def test___eq__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertTrue(
            context.model['mybool'] == context.model['mybool'],
            "The equality must be correct"
        )

    def test___iter__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            list(iter(context.model['mybool'])),
            ['0', '1'],
            "The iter must be correct"
        )

    def test___str__(self):
        context = MemoryContext(
            definition={'mybool': bool, 'myint': int},
            individuals=['0', '1']
        )
        self.assertEqual(
            str(context.model['mybool']),
            "{'name': 'mybool', 'type': <class 'bool'>}",
            "The iter must be correct"
        )
