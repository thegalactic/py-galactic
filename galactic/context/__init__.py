# This Python file uses the following encoding: utf-8
"""
The :mod:`galactic.context` package defines generic classes for using contexts:

* :class:`Context`: a context is composed by a population and a model
* :class:`Population` a population is a container for individuals
* :class:`Model` a model is a container for attributes
* :class:`Individual` an individual has an identifier and values
* :class:`Attribute` an attribute has a name and a type
"""

from abc import abstractmethod
from typing import Container, Union, Mapping, Iterator, TypeVar, Generic

C = TypeVar('C', bound='Context')
"""
Generic subclass of the :class:`Context` class
"""

P = TypeVar('P', bound='Population')
"""
Generic subclass of the :class:`Population` class
"""

M = TypeVar('M', bound='Model')
"""
Generic subclass of the :class:`Model` class
"""

X = TypeVar('X', bound='Individual')
"""
Generic subclass of the :class:`Individual` class
"""

A = TypeVar('A', bound='Attribute')
"""
Generic subclass of the :class:`Attribute` class
"""


# pylint: disable=too-few-public-methods
class Context(Generic[M, P, X, A], Container[Union[X, A]]):
    """
    A :class:`Context` handles a model and a population.

    It's possible to access to the context :attr:`population` attribute or to
    the context :attr:`model` attribute.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> print(context.population)
        ['0', '1']
        >>> print(context.model)
        {'mybool': <class 'bool'>, 'myint': <class 'int'>}

    It's possible to check if a context is not empty (both :attr:`model` and :attr:`population`
    are not empty) using the python builtin :func:`bool` function.

    It's possible to get a readable representation of a context using the python builtin :func:`str`
    function.

    Example
    -------

        >>> print(context)
        {'population': ['0', '1'], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    Example
    -------

        >>> bool(context)
        True

    Contexts are container for individuals and attributes. It's possible to know if an individual
    or an attribute belongs to a context using the python :keyword:`in` keyword.

    Example
    -------

        >>> context.model['mybool'] in context
        True
        >>> context.population['0'] in context
        True

    .. versionadded:: 0.0.1
    """

    @property
    @abstractmethod
    def population(self) -> P:
        """
        Get the population for this context.

        Returns
        -------
            the underlying population : :class:`P`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> M:
        """
        Get the underlying model.

        Returns
        -------
            the underlying model : :class:`M`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    def __contains__(self, element: Union[X, A]):
        """
        Check if an individual or an attribute is in this context.

        Parameters
        ----------
            element : Union[:class:`X`, :class:`A`]
                the element to check

        Returns
        -------
            the membership of the element to the context : :class:`bool`

        .. versionadded:: 0.0.1
        """
        return element.context == self

    def __bool__(self):
        """
        Check if this context is not empty.

        Returns
        -------
            True if it contains some attribute and some individuals : :class:`bool`


        .. versionadded:: 0.0.1
        """
        return bool(self.population) and bool(self.model)

    def __str__(self):
        """
        Convert this context to a readable string.

        Returns
        -------
            the user friendly readable string of this context : :class:`str`

        .. versionadded:: 0.0.1
        """
        return str({
            'population': [identifier for identifier in self.population],
            'model': {name: attribute.type for name, attribute in self.model.items()}
        })


# pylint: disable=too-few-public-methods,function-redefined
class Population(Generic[C, M, X], Mapping[str, X]):
    """
    A :class:`Population` is a container for individuals.

    It's possible to access to the population :attr:`context` attribute.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> population = context.population
        >>> print(population.context)
        {'population': ['0', '1'], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    It's possible to get a readable representation of a population.

    Example
    -------

        >>> print(population)
        ['0', '1']

    It's possible to check if a population is not empty using the python builtin :func:`bool`
    function.

    Example
    -------

        >>> bool(population)
        True

    It's possible to access to an individual with its identifier using the python array access
    construct.

    Example
    -------

        >>> print(population['0'])
        {'mybool': False, 'myint': 0}

    It's possible to check if an individual belongs to a population using the python
    :keyword:`in` keyword.

    Example
    -------

        >>> '0' in population
        True

    It's possible to iterate over a population using the python :keyword:`for` keyword.

    Example
    -------

        >>> {ident: str(individual) for ident, individual in population.items()}
        {'0': "{'mybool': False, 'myint': 0}", '1': "{'mybool': False, 'myint': 0}"}

    It's possible to get the length of a population using the python builtin :func:`len`
    function.

    Example
    -------

        >>> len(population)
        2

    .. versionadded:: 0.0.1
    """

    @property
    @abstractmethod
    def context(self) -> C:
        """
        Get the underlying context.

        Returns
        -------
            the underlying context : :class:`C`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    def model(self) -> M:
        """
        Get the underlying model.

        Returns
        -------
            the underlying model : :class:`M`

        .. versionadded:: 0.0.1
        """
        return self.context.model

    @abstractmethod
    def __bool__(self):
        """
        Check if this population is not empty.

        Returns
        -------
            True if this population is not empty : :class:`bool`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    def __str__(self):
        """
        Convert this population to a readable string.

        Returns
        -------
            the user friendly readable string of this population : :class:`str`

        .. versionadded:: 0.0.1
        """
        return str([identifier for identifier in self])


class Model(Generic[C, P, A],
            Mapping[str, A]):  # pylint: disable=too-few-public-methods,function-redefined
    """
    A :class:`Model` is a container for attributes.

    It's possible to access to the model :attr:`context` attribute.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> model = context.model
        >>> print(model.context)
        {'population': ['0', '1'], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    It's possible to get a readable representation of a model using the python builtin :func:`str`
    function.

    Example
    -------

        >>> print(model)
        {'mybool': <class 'bool'>, 'myint': <class 'int'>}

    It's possible to check if a model is not empty using the python builtin :func:`bool` function.

    Example
    -------

        >>> bool(model)
        True

    It's possible to access to an attribute with its name using the python array access
    construct.

    Example
    -------

        >>> print(model['mybool'])
        {'name': 'mybool', 'type': <class 'bool'>}

    It's possible to check if an attribute belongs to a model using the python
    :keyword:`in` keyword.

    Example
    -------

        >>> 'mybool' in model
        True

    It's possible to iterate over a model using the python :keyword:`for` keyword.

    Example
    -------

        >>> {name: attribute.type for name, attribute in model.items()}
        {'mybool': <class 'bool'>, 'myint': <class 'int'>}

    It's possible to get the length of a population using the python builtin :func:`len`
    function.

    Example
    -------

        >>> len(model)
        2

    .. versionadded:: 0.0.1
    """

    @property
    @abstractmethod
    def context(self) -> C:
        """
        Get the underlying context.

        Returns
        -------
            the underlying context : :class:`C`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    def population(self) -> P:
        """
        Get the underlying population.

        Returns
        -------
            the underlying population : :class:`P`

        .. versionadded:: 0.0.1
        """
        return self.context.population

    @abstractmethod
    def __bool__(self):
        """
        Check if this model is not empty.

        Returns
        -------
            True if this model is not empty : :class:`bool`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    def __str__(self):
        """
        Convert this model to a readable string.

        Returns
        -------
            the user friendly readable string of this model : :class:`str`

        .. versionadded:: 0.0.1
        """
        return str({name: attribute.type for name, attribute in self.items()})


# pylint: disable=too-few-public-methods,function-redefined
class Individual(Generic[C, P, M, X, A], Mapping[str, object]):
    """
    A :class:`Individual` is a container for values.

    It's possible to access to the individual :attr:`identifier` attribute.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> individual = context.population['0']
        >>> individual.identifier
        '0'

    It's possible to access to the individual :attr:`context` attribute.

    Example
    -------

        >>> print(individual.context)
        {'population': ['0', '1'], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    It's possible to access to the individual :attr:`model` attribute.

    Example
    -------

        >>> print(individual.model)
        {'mybool': <class 'bool'>, 'myint': <class 'int'>}

    It's possible to access to the individual :attr:`population` attribute.

    Example
    -------

        >>> print(individual.population)
        ['0', '1']

    It's possible to get a readable representation of an individual using the python builtin
    :func:`str` function.

    Example
    -------

        >>> print(individual)
        {'mybool': False, 'myint': 0}

    It's possible to access to the individual values using the :meth:`value` method.

    Example
    -------

        >>> attribute = individual.model['mybool']
        >>> individual.value(attribute)
        False

    It's possible to access to the individual values using the python array access
    construct.

    Example
    -------

        >>> individual['mybool']
        False

    It's possible to get the length of an individual using the python builtin :func:`len`
    function.

    Example
    -------

        >>> len(individual)
        2

    It's possible to iterate over an individual using the python :keyword:`for` keyword.

    Example
    -------

        >>> {name: value for name, value in individual.items()}
        {'mybool': False, 'myint': 0}

    .. versionadded:: 0.0.1
    """

    @property
    @abstractmethod
    def identifier(self) -> str:
        """
        Get this individual identifier.

        Returns
        -------
            the individual identifier : :class:`str`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def population(self) -> P:
        """
        Get the underlying population.

        Returns
        -------
            the underlying population : :class:`P`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    def context(self) -> C:
        """
        Get the underlying context.

        Returns
        -------
            the underlying context : :class:`C`

        .. versionadded:: 0.0.1
        """
        return self.population.context

    @property
    def model(self) -> M:
        """
        Get the underlying model.

        Returns
        -------
            the underlying model : :class:`M`

        .. versionadded:: 0.0.1
        """
        return self.context.model

    def value(self, attribute: A):
        """
        Get the attribute value for this individual.

        Parameters
        ----------
            attribute : :class:`A`
                the attribute

        Returns
        -------
            the value : :class:`object`

        Raises
        ------
            ValueError
                if the attribute does not belong to the underlying model.

        .. versionadded:: 0.0.1
        """
        if attribute.context == self.context:
            return self[attribute.name]
        else:
            raise ValueError

    @abstractmethod
    def __getitem__(self, name: str):
        """
        Get the value of this individual for the given attribute. The :param name: is the attribute
        name.

        Parameters
        ----------
            name : :class:`str`
                the attribute name

        Returns
        -------
            the associated value : :class:`object`

        Raises
        ------
            KeyError
                if the attribute does not belong to the underlying model.

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    def __iter__(self) -> Iterator[str]:
        """
        Get an iterator for this individual.

        Returns
        -------
            an iterator : :class:`<Iterator[str] <python:collections.abc.iterator>`

        .. versionadded:: 0.0.1
        """
        return iter(self.model)

    def __len__(self):
        """
        Get the length of this individual.

        Returns
        -------
            the length of this individual : :class:`int`

        .. versionadded:: 0.0.1
        """
        return len(self.model)

    def __eq__(self, other: X):
        """
        Check if two individuals are equal.

        Parameters
        ----------
            other : :class:`X`
                the individual to test the equality with

        Returns
        -------
            self == other : :class:`bool`

        .. versionadded:: 0.0.1
        """
        return self.identifier == other.identifier and self.context == other.context

    def __hash__(self):
        """
        Use specific hashing.

        Returns
        -------
            the hash number : :class:`int`

        .. versionadded:: 0.0.1
        """
        return hash((self.identifier, self.context))

    def __str__(self):
        """
        Convert this individual to a readable string.

        Returns
        -------
            the user friendly readable string of this individual : :class:`str`

        .. versionadded:: 0.0.1
        """
        return str({name: value for name, value in self.items()})


# pylint: disable=too-few-public-methods,function-redefined
class Attribute(Generic[C, P, M, X, A], Mapping[str, object]):
    """
    A :class:`Attribute` is described by a :attr:`name` and a :attr:`type`.

    It's possible to access to the attribute :attr:`identifier` and :attr:`type` attributes.

    Example
    -------

        >>> from galactic.context.memory import MemoryContext
        >>> context = MemoryContext(
        ...     definition={'mybool': bool, 'myint': int},
        ...     individuals=['0', '1']
        ... )
        >>> attribute = context.model['mybool']
        >>> attribute.name
        'mybool'
        >>> attribute.type
        <class 'bool'>

    It's possible to access to the individual :attr:`context` attribute.

    Example
    -------

        >>> print(attribute.context)
        {'population': ['0', '1'], 'model': {'mybool': <class 'bool'>, 'myint': <class 'int'>}}

    It's possible to access to the individual :attr:`model` attribute.

    Example
    -------

        >>> print(attribute.model)
        {'mybool': <class 'bool'>, 'myint': <class 'int'>}

    It's possible to access to the individual :attr:`population` attribute.

    Example
    -------

        >>> print(attribute.population)
        ['0', '1']

    It's possible to get a readable representation of an attribute using the python builtin
    :func:`str` function.

    Example
    -------

        >>> print(attribute)
        {'name': 'mybool': 'type': <class 'bool'>}

    It's possible to access to the attribute values using the :meth:`value` method.

    Example
    -------

        >>> individual = attribute.population['0']
        >>> attribute.value(individual)
        False

    It's possible to access to the attribute values using the python array access
    construct.

    Example
    -------

        >>> attribute['0']
        False

    It's possible to get the length of an attribute using the python builtin :func:`len`
    function.

    Example
    -------

        >>> len(attribute)
        2

    It's possible to iterate over an attribute using the python :keyword:`for` keyword.

    Example
    -------

        >>> {identifier: value for identifier, value in attribute.items()}
        {'0': False, '1': False}

    .. versionadded:: 0.0.1
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the attribute name.

        Returns
        -------
            the attribute name : :class:`str`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> type:
        """
        Get the attribute type.

        Returns
        -------
            the attribute type : :class:`type <python:type>`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> M:
        """
        Get the underlying model.

        Returns
        -------
            the underlying model : :class:`M`

        .. versionadded:: 0.0.1
        """
        raise NotImplementedError

    @property
    def context(self) -> C:
        """
        Get the underlying context.

        Returns
        -------
            the underlying context : :class:`C`

        .. versionadded:: 0.0.1
        """
        return self.model.context

    @property
    def population(self) -> P:
        """
        Get the underlying population.

        Returns
        -------
            the underlying population : :class:`P`

        .. versionadded:: 0.0.1
        """
        return self.context.population

    def value(self, individual: X):
        """
        Get the individual value for this attribute.

        Parameters
        ----------
            individual : :class:`X`
                the individual

        Returns
        -------
            the value : :class:`object`

        Raises
        ------
            ValueError
                if the individual does not belong to the underlying population.

        .. versionadded:: 0.0.1
        """
        return individual.value(self)

    def __getitem__(self, identifier: str):
        """
        Get the value of this attribute for the given individual.

        Parameters
        ----------
            identifier : :class:`str`
                the individual identifier

        Returns
        -------
            the value : :class:`object`

        Raises
        ------
            KeyError
                if the individual does not belong to the underlying population.

        .. versionadded:: 0.0.1
        """
        return self.population[identifier][self.name]

    def __iter__(self) -> Iterator[str]:
        """
        Get the iterator of this attribute.

        Returns
        -------
            an iterator : :class:`Iterator[Individual] <python:collections.abc.iterator>`

        .. versionadded:: 0.0.1
        """
        return iter(self.population)

    def __len__(self):
        """
        Get the length of this attribute.

        Returns
        -------
            the length of this attribute : :class:`int`

        .. versionadded:: 0.0.1
        """
        return len(self.population)

    def __eq__(self, other: A):
        """
        Check if two attributes are equal.

        Parameters
        ----------
            other : :class:`A`
                the attribute to test the equality with

        Returns
        -------
            self == other : :class:`bool`

        .. versionadded:: 0.0.1
        """
        return self.name == other.name and self.context == other.context

    def __hash__(self):
        """
        Use specific hashing.

        Returns
        -------
            the hash number : :class:`int`

        .. versionadded:: 0.0.1
        """
        return hash((self.name, self.context))

    def __str__(self):
        """
        Convert this attribute to a printable string.

        Returns
        -------
            the user friendly readable string of this attribute : :class:`str`

        .. versionadded:: 0.0.1
        """
        return str({'name': self.name, 'type': self.type})
