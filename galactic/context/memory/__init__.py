# This Python file uses the following encoding: utf-8

"""
The :mod:`galactic.context.memory` module give the ability to define
:class:`Context <galactic.context.Context>` that resides in memory.
"""

from typing import Mapping, Iterable, Union

from galactic.context import Context, Model, Population, Attribute, Individual
from galactic.context.mixins import ContextHolder, PopulationHolder, ModelHolder, \
    ConcreteAttribute, ConcreteIndividual, AttributesHolder, IndividualsHolder, ValuesHolder


# pylint: disable=too-few-public-methods,abstract-method,super-init-not-called
class MemoryContext(
        PopulationHolder['MemoryPopulation'],
        ModelHolder['MemoryModel'],
        Context['MemoryPopulation', 'MemoryModel', 'MemoryIndividual', 'MemoryAttribute']
):
    """
    The :class:`MemoryContext` class is designed to define contexts in memory. It inherits of all
    the behavior from the :class:`Context <galactic.context.Context>` class and allows direct
    creation and modification of a context.

    It's possible to create a context without nothing.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext()
        >>> print(context)
        {'population': [], 'model': {}}

    It's possible to create a context specifying the model definition.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(definition={'mybool': bool, 'myint': int})
        >>> print(context)
        {'population': [], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    It's possible to create a context specifying the model definition and the list of individual
    identifiers.

    Example
    -------

        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> print(context)
        {'population': ['0', '1'], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    It's possible to create a context specifying the model definition and the individual values.

    Example
    -------

        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals={'0': {'mybool': True}, '1':{'myint': 1}}
        ... )
        >>> {ident: str(context.population[ident]) for ident in context.population}
        {'0': "{'mybool': True, 'myint': 0}", '1': "{'mybool': False, 'myint': 1}"}

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise a context in memory.

        Keyword Arguments
        -----------------
            definition : :class:`Mapping[str, type] <python:collections.abc.Mapping>`
                definition of the context by a mapping from name of attributes to their type
            individuals : :class:`Union[Iterable[str], Mapping[str, Mapping[str, object]]]`
                initial iterable of individual identifiers or a mapping from individual
                identifiers to individual values

        Raises
        ------
            KeyError
                if an attribute is not in the definition
            ValueError
                if a value does not correspond to an attribute type
            TypeError
                if the definition or if the individuals parameter are not of the correct type

        .. versionadded:: 0.0.1
        """
        definition = MemoryContext._definition(**kwargs)
        individuals = MemoryContext._individuals(**kwargs)

        super().__init__(
            model=MemoryModel(self, {} if definition is None else definition),
            population=MemoryPopulation(self, [])
        )

        if isinstance(individuals, Mapping):
            for identifier, values in individuals.items():
                self.population[identifier] = values
        else:
            if individuals is not None:
                for identifier in individuals:
                    self.population[identifier] = {}

    @staticmethod
    def _definition(**kwargs) -> Mapping[str, type]:
        """
        Get the definition from the keyword arguments.

        Keyword arguments
        -----------------
            definition : :class:`Mapping[str, type] <python:collections.abc.Mapping>`
                definition of the context by a mapping from name of attributes to their type

        Raises
        ------
            TypeError
                if the definition parameter is not of the correct type

        .. versionadded:: 0.0.2
        """
        if 'definition' in kwargs:
            definition = kwargs['definition']
            if not isinstance(definition, Mapping):
                raise TypeError
        else:
            definition = None
        return definition

    @staticmethod
    def _individuals(**kwargs) -> Union[Iterable[str], Mapping[str, Mapping[str, object]]]:
        """
        Get the individuals from the keyword arguments.

        Keyword arguments
        -----------------
            individuals : :class:`Union[Iterable[str], Mapping[str, Mapping[str, object]]]`
                initial iterable of individual identifiers or a mapping from individual
                identifiers to individual values

        Raises
        ------
            TypeError
                if the definition parameter is not of the correct type

        .. versionadded:: 0.0.2
        """
        if 'individuals' in kwargs:
            individuals = kwargs['individuals']
            if not isinstance(individuals, (Iterable, Mapping)):
                raise TypeError
        else:
            individuals = None
        return individuals


# pylint: disable=too-few-public-methods,abstract-method,super-init-not-called
class MemoryModel(
        ContextHolder[MemoryContext],
        AttributesHolder['MemoryAttribute'],
        Model[MemoryContext, 'MemoryPopulation', 'MemoryAttribute']
):
    """
    The :class:`MemoryModel` class is designed to define models that resides in memory. It inherits
    of all the behavior from the :class:`Model <galactic.context.Model>` class.

    It's possible to change or to set attribute values.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> model = context.model
        >>> model['mybool'] = int
        >>> model['myint2'] = int
        >>> print(context.population['0'])
        {'mybool': 0, 'myint': 0, 'myint2': 0}

    It's possible to delete an attribute using its name.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> model = context.model
        >>> del model['mybool']
        >>> {ident: str(context.population[ident]) for ident in context.population}
        {'0': "{'myint': 0}", '1': "{'myint': 0}"}


    .. versionadded:: 0.0.1
    """

    def __init__(
            self,
            context: MemoryContext,
            definition: Mapping[str, 'type']
    ):
        """
        Initialise a model in memory.

        Parameters
        ----------
            context : :class:`MemoryContext`
                the underlying context
            definition : :class:`Mapping[str, type] <python:collections.abc.Mapping>`
                the attributes definition

        .. versionadded:: 0.0.1
        """
        super().__init__(
            context=context,
            attributes=[MemoryAttribute(self, name, cls) for name, cls in definition.items()]
        )

    def __delitem__(self, name: str):
        """
        Delete an attribute from a :class:`MemoryModel`.

        Parameters
        ----------
            name : :class:`str`
                attribute name

        Raises
        ------
            KeyError
                if the attribute is not in the model

        .. versionadded:: 0.0.1
        """
        super().__delitem__(name)
        for identifier in self.population:
            del self.population[identifier][name]

    def __setitem__(self, name: str, cls: type):
        """
        Set an attribute for a :class:`MemoryModel`.

        Parameters
        ----------
            name : :class:`str`
                the attribute name
            cls : :class:`python:type`
                the attribute type

        .. versionadded:: 0.0.1
        """
        if name in self:
            if self[name].type != cls:
                super().__setitem__(name, MemoryAttribute(self, name, cls))
                for identifier in self.population:
                    try:
                        self.population[identifier][name] = cls(self.population[identifier][name])
                    except (ValueError, TypeError):
                        self.population[identifier][name] = cls()
        else:
            super().__setitem__(name, MemoryAttribute(self, name, cls))
            for identifier in self.population:
                self.population[identifier][name] = cls()


# pylint: disable=too-few-public-methods,abstract-method,super-init-not-called
class MemoryPopulation(
        ContextHolder[MemoryContext],
        IndividualsHolder['MemoryIndividual'],
        Population[MemoryContext, MemoryModel, 'MemoryIndividual']
):
    """
    The :class:`MemoryPopulation` class is designed to define populations that resides in memory. It
    inherits of all the behavior from the :class:`Population <galactic.context.Population>` class.

    It's possible to change or to set individual values.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> population = context.population
        >>> population['0'] = {'mybool': True}
        >>> population['2'] = {'myint': 1}
        >>> print(population['0'])
        {'mybool': True, 'myint': 0}
        >>> print(population['2'])
        {'mybool': False, 'myint': 1}

    It's possible to delete an individual using its identifier.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> population = context.population
        >>> del population['0']
        >>> {ident: str(context.population[ident]) for ident in context.population}
        {'1': "{'mybool': False, 'myint': 0}"}

    .. versionadded:: 0.0.1
    """

    def __init__(
            self,
            context: MemoryContext,
            identifiers: Iterable[str]
    ):
        """
        Initialise a population in memory.

        Parameters
        ----------
            context : :class:`MemoryContext`
                the underlying context
            identifiers : :class:`Iterable[str] <python:collections.abc.Iterable>`
                an iterable of identifiers

        .. versionadded:: 0.0.1
        """
        super().__init__(
            context=context,
            individuals=[MemoryIndividual(self, identifier) for identifier in identifiers]
        )

    def __setitem__(self, identifier: str, values: Mapping[str, object]):
        """
        Set an individual for a :class:`MemoryPopulation`.

        Parameters
        ----------
            identifier : :class:`str`
                the individual identifier
            values : :class:`Mapping[str, object] <<python:collections.abc.mapping>>`
                the initial values for some attributes

        Raises
        ------
            KeyError
                if an attribute name does not belong to the underlying model.
            ValueError
                if an attribute value does not correspond to its type

        .. versionadded:: 0.0.1
        """
        try:
            individual = self[identifier]
        except KeyError:
            individual = MemoryIndividual(self, identifier)
            super().__setitem__(identifier, individual)
        for name, value in values.items():
            if name not in self.model:
                raise KeyError
            individual[name] = value


# pylint: disable=too-few-public-methods,abstract-method,super-init-not-called
class MemoryIndividual(
        PopulationHolder[MemoryPopulation],
        ValuesHolder,
        ConcreteIndividual,
        Individual[
            MemoryContext,
            MemoryPopulation,
            MemoryModel,
            'MemoryIndividual',
            'MemoryAttribute'
        ]
):
    """
    The :class:`MemoryIndividual` is designed to define individuals that resides in memory. It
    inherits of all the behavior from the :class:`Individual <galactic.context.Individual>` class.

    It's possible to modify a value for an individual using an attribute name.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> individual = context.population['0']
        >>> individual['mybool'] = True
        >>> individual['myint'] = 1
        >>> {ident: str(context.population[ident]) for ident in context.population}
        {'0': "{'mybool': True, 'myint': 1}", '1': "{'mybool': False, 'myint': 0}"}

    .. versionadded:: 0.0.1
    """

    def __init__(
            self,
            population: MemoryPopulation,
            identifier: str
    ):
        """
        Initialise an individual.

        Parameters
        ----------
            population : :class:`MemoryPopulation`
                the population
            identifier : :class:`str`
                the individual identifier

        .. versionadded:: 0.0.1
        """
        super().__init__(
            population=population,
            identifier=identifier,
            values={name: attribute.type() for name, attribute in population.model.items()}
        )

    def __setitem__(self, name: str, value):
        """
        Set an individual's attribute value using either the attribute or its name.

        Parameters
        ----------
            name: :class:`str`
                the attribute name
            value : :class:`object`
                the value

        Raises
        ------
            KeyError
                if the attribute does not belong to the underlying context
            ValueError
                if the value passed in argument has its type different of the attribute type

        .. versionadded:: 0.0.1
        """
        attribute = self.model[name]
        if not isinstance(value, attribute.type):
            value = attribute.type(value)
        super().__setitem__(name, value)

    def __delitem__(self, name: str):
        """
        Delete an individual value.

        Parameters
        ----------
            name: :class:`str`
                the attribute name

        Raises
        ------
            ValueError
                if the attribute is in the model (which should be always the case)

        .. versionadded:: 0.0.1
        """
        if name in self.model:
            raise ValueError
        else:
            super().__delitem__(name)


# pylint: disable=too-few-public-methods,abstract-method,super-init-not-called
class MemoryAttribute(
        ModelHolder[MemoryModel],
        ConcreteAttribute,
        Attribute[
            MemoryContext,
            MemoryPopulation,
            MemoryModel,
            MemoryIndividual,
            'MemoryAttribute'
        ]
):
    """
    The :class:`MemoryAttribute` is designed to define attributes that resides in memory. It
    inherits of all the behavior from the :class:`Attribute <galactic.context.Attribute>` class.

    It's possible to modify a value for an attribute using an individual identifier.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> attribute = context.model['myint']
        >>> attribute['0'] = 3
        >>> attribute['1'] = 4
        >>> {ident: str(context.population[ident]) for ident in context.population}
        {'0': "{'mybool': False, 'myint': 3}", '1': "{'mybool': False, 'myint': 4}"}

    .. versionadded:: 0.0.1
    """

    def __init__(
            self,
            model: MemoryModel,
            name: str,
            cls: 'type'
    ):
        """
        Initialise an attribute.

        Parameters
        ----------
            model : :class:`MemoryModel`
                the underlying model
            name : :class:`str`
                the attribute name
            cls : :class:`type <python:type>`
                the attribute type

        .. versionadded:: 0.0.1
        """
        super().__init__(
            model=model,
            name=name,
            type=cls
        )

    def __setitem__(self, identifier: str, value):
        """
        Set an individual's attribute value using either the individual or its identifier.

        This method raises a :class:`KeyError` exception if the attribute does not belong to
        the underlying context and a :class:`ValueError` exception if the value passed in argument
        has its type different of the attribute type.

        Parameters
        ----------
            identifier : :class:`str`
                the individual identifier
            value : :class:`object`
                the value

        Raises
        ------
            KeyError
                if the individual does not exists
            ValueError
                if the value is not of the attribute type

        .. versionadded:: 0.0.1
        """
        self.population[identifier][self.name] = value
