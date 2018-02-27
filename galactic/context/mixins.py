# This Python file uses the following encoding: utf-8
"""
The :mod:`galactic.context.mixins` package defines mixins classes for defining new types of
contexts:

* :class:`ConcreteIndividual` for defining individuals that own their identifier as a field
* :class:`ConcreteAttribute` for defining attributes that own their name and their type as fields
* :class:`ContextHolder` for defining elements that own their context as a field
* :class:`PopulationHolder` for defining elements that own their population as a field
* :class:`ModelHolder` for defining elements that own their model as a field
* :class:`AttributesHolder` for defining models that own their attributes as a field
* :class:`IndividualsHolder` for defining population that own their individuals as a field
* :class:`ValuesHolder` for defining individuals that own their values as a field

They are widely used for defining

* :class:`MemoryContext <galactic.context.memory.MemoryContext>`
* :class:`MemoryModel <galactic.context.memory.MemoryModel>`
* :class:`MemoryPopulation <galactic.context.memory.MemoryPopulation>`
* :class:`MemoryAttribute <galactic.context.memory.MemoryAttribute>`
* :class:`MemoryIndividual <galactic.context.memory.MemoryIndividual>`

in the :mod:`galactic.context.memory` package.

.. versionadded:: 0.0.1
"""

from typing import Generic, MutableMapping, Iterator

from galactic.context import C, P, M, A, X


# pylint: disable=too-few-public-methods
class _Mixin(object):
    def __init__(self, **_):
        super().__init__()


# pylint: disable=too-few-public-methods,function-redefined
class ConcreteIndividual(_Mixin):
    """
    The :class:`ConcreteIndividual` class is a mixin used in subclassing the
    :class:`Individual <galactic.context.Individual>` class for storing their identifier as a field.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an individual.

        Keyword Arguments
        -----------------
            identifier : :class:`str`
                the individual identifier

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._identifier = kwargs['identifier']

    @property
    def identifier(self) -> str:
        """
        Get the individual identifier.

        Returns
        -------
            the individual identifier : :class:`str`

        .. versionadded:: 0.0.1
        """
        return self._identifier


# pylint: disable=too-few-public-methods
class ConcreteAttribute(_Mixin):
    """
    The :class:`ConcreteAttribute` class is a mixin used in subclassing the
    :class:`Attribute <galactic.context.Attribute>` class for storing their name and their type
    as a class.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an attribute

        Keyword Arguments
        -----------------
            name : :class:`str`
                the attribute name

            type : :class:`type <python:type>`
                the attribute type

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._name = kwargs['name']
        self._type = kwargs['type']

    @property
    def name(self) -> str:
        """
        Get the attribute name.

        Returns
        -------
            the attribute name : :class:`str`

        .. versionadded:: 0.0.1
        """
        return self._name

    @property
    def type(self) -> type:
        """
        Get the attribute type.

        Returns
        -------
            the attribute type : :class:`type <python:type>`

        .. versionadded:: 0.0.1
        """
        return self._type


# pylint: disable=too-few-public-methods
class ContextHolder(_Mixin, Generic[C]):
    """
    The :class:`ContextHolder[C] <ContextHolder>` is a mixin used for storing an element context as
    a field.

    It's a generic class that depends of a :class:`Context <galactic.context.Context>` subclass
    :class:`C`.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an element by setting its context.

        Keyword Arguments
        -----------------
            context : :class:`C`
                the context

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._context = kwargs['context']

    # noinspection PyTypeChecker
    @property
    def context(self) -> C:
        """
        Get the context.

        Returns
        -------
            the context : :class:`C`

        .. versionadded:: 0.0.1
        """
        return self._context


# pylint: disable=too-few-public-methods
class PopulationHolder(_Mixin, Generic[P]):
    """
    The :class:`PopulationHolder[P] <PopulationHolder>` is a mixin used for storing an element
    population as a field.

    It's a generic class that depends of a :class:`Population <galactic.context.Population>`
    subclass :class:`P`.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an element by setting its population.

        Keyword Arguments
        -----------------
            population: :class:`P`
                the population

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._population = kwargs['population']

    # noinspection PyTypeChecker
    @property
    def population(self) -> P:
        """
        Get the population.

        Returns
        -------
            the population : :class:`P`

        .. versionadded:: 0.0.1
        """
        return self._population


# pylint: disable=too-few-public-methods
class ModelHolder(_Mixin, Generic[M]):
    """
    The :class:`ModelHolder[M] <ModelHolder>` class is a mixin used for storing an element model as
    a field.

    It's a generic class that depends of a :class:`Model <galactic.context.Model>` subclass
    :class:`M`.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an element by setting its model.

        Keyword Arguments
        -----------------
            model : :class:`M`
                the model

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._model = kwargs['model']

    # noinspection PyTypeChecker
    @property
    def model(self) -> M:
        """
        Get the model.

        Returns
        -------
            the model : :class:`M`

        .. versionadded:: 0.0.1
        """
        return self._model


# pylint: disable=too-few-public-methods
class AttributesHolder(_Mixin, Generic[A], MutableMapping[str, A]):
    """
    The :class:`AttributesHolder[A] <AttributesHolder>` class is a mixin used for storing the model
    attributes in memory.

    It's a generic class that depends of an :class:`Attribute <galactic.context.Attribute>`
    subclass :class:`A`.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an attribute holder.

        Keyword Arguments
        -----------------
            attributes : :class:`Iterable[A] <python:collections.abc.Iterable>`
                the attributes

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._attributes = {attribute.name: attribute for attribute in kwargs['attributes']}

    def __getitem__(self, name: str) -> A:
        """
        Get an attribute using its name

        Parameters
        ----------
            name : :class:`str`
                the attribute name

        Returns
        -------
            the attribute : A

        Raises
        ------
            KeyError
                if this attributes holder does not contain an attribute with this name.

        .. versionadded:: 0.0.1
        """
        return self._attributes[name]

    def __setitem__(self, name: str, attribute: A) -> None:
        """
        Set an attribute using its name

        Parameters
        ----------
            name : :class:`str`
                the attribute name
            attribute: :class:`A`

        .. versionadded:: 0.0.1
        """
        self._attributes[name] = attribute

    def __delitem__(self, name: str) -> None:
        """
        Delete an attribute using its name

        Parameters
        ----------
            name : :class:`str`
                the attribute name

        Raises
        ------
            KeyError
                if this attributes holder does not contain an attribute with this name.

        .. versionadded:: 0.0.1
        """
        del self._attributes[name]

    def __iter__(self) -> Iterator[str]:
        """
        Get an iterator over the attribute names.

        Returns
        -------
            an iterator : :class:`Iterator[str] <python:collections.abc.Iterator>`

        .. versionadded:: 0.0.1
        """
        return iter(self._attributes)

    def __len__(self) -> int:
        """
        Get the number of attributes.

        Returns
        -------
            the number of attributes : :class:`int`

        .. versionadded:: 0.0.1
        """
        return len(self._attributes)

    def __bool__(self):
        """
        Get the boolean value of an attribute holder.

        Returns
        -------
            the boolean value : :class:`bool`

        .. versionadded:: 0.0.1
        """
        return bool(self._attributes)


# pylint: disable=too-few-public-methods
class IndividualsHolder(_Mixin, Generic[X], MutableMapping[str, X]):
    """
    The :class:`IndividualsHolder[X] <IndividualsHolder>` class  is a mixin used for storing the
    population individuals in memory.

    It's a generic class that depends of an :class:`Individual <galactic.context.Individual>`
    subclass :class:`X`.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise an individuals holder.

        Keyword Arguments
        -----------------
            individuals : :class:`Iterable[A] <python:collections.abc.Iterable>`
                the individuals

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._individuals = {individual.identifier: individual for individual in
                             kwargs['individuals']}

    def __getitem__(self, identifier: str) -> X:
        """
        Get an individual using its identifier.

        Parameters
        ----------
            identifier : :class:`str`
                the individual identifier

        Returns
        -------
            the individual : :class: `X`

        Raises
        ------
            KeyError
                if the identifier does not belong to the individuals holder.

        .. versionadded:: 0.0.1
        """
        return self._individuals[identifier]

    def __delitem__(self, identifier: str) -> None:
        """
        Delete an individual using its identifier.

        Parameters
        ----------
            identifier : :class:`str`
                the individual identifier

        Raises
        ------
            KeyError
                if the identifier does not belong to the individuals holder.

        .. versionadded:: 0.0.1
        """
        del self._individuals[identifier]

    def __setitem__(self, identifier: str, individual: X) -> None:
        """
        Set an individual using its identifier.

        Parameters
        ----------
            identifier : :class:`str`
                the individual identifier

            individual: :class:`X`
                an individual

        .. versionadded:: 0.0.1
        """
        self._individuals[identifier] = individual

    def __iter__(self) -> Iterator[str]:
        """
        Get an iterator over the individual identifiers.

        Returns
        -------
            an iterator : :class:`Iterator[str] <python:collections.abc.Iterator>`

        .. versionadded:: 0.0.1
        """
        return iter(self._individuals)

    def __len__(self) -> int:
        """
        Get the number of individuals.

        Returns
        -------
            the number of indidivuals : :class:`int`

        .. versionadded:: 0.0.1
        """
        return len(self._individuals)

    def __bool__(self) -> bool:
        """
        Get the boolean representation of the individuals holder.

        Returns
        -------
            the boolean representation : :class:`bool`

        .. versionadded:: 0.0.1
        """
        return bool(self._individuals)


# pylint: disable=too-few-public-methods
class ValuesHolder(_Mixin):
    """
    The :class:`ValuesHolder[A] <ValuesHolder>` class is a mixin for storing the individual values
    in memory.

    It's a generic class that depends of an :class:`Attribute <galactic.context.Attribute>` subclass
    :class:`A`.

    .. versionadded:: 0.0.1
    """

    def __init__(self, **kwargs):
        """
        Initialise a values holder.

        Keyword Arguments
        -----------------
            values : :class:`Mapping[str, object] <python:collections.abc.Mapping>`
                the initial (name, value) pairs

        .. versionadded:: 0.0.1
        """
        super().__init__(**kwargs)
        self._values = {name: value for name, value in kwargs['values'].items()}

    def __getitem__(self, name: str) -> object:
        """
        Get a value using the attribute name.

        Parameters
        ----------
            name : :class:`str`
                the attribute name

        Returns
        -------
            the value : :class:`object`

        Raises
        ------
            KeyError
                if the name does not belong to the values holder.

        .. versionadded:: 0.0.1
        """
        return self._values[name]

    def __setitem__(self, name: str, value) -> None:
        """
        Set the value of an attribute.

        Parameters
        ----------
            name : :class:`str`
                the attribute name
            value : :class:`object`
                the new value

        .. versionadded:: 0.0.1
        """
        self._values[name] = value

    def __delitem__(self, name: str):
        """
        Delete a value using the attribute name.

        Parameters
        ----------
            name : :class:`str`
                the attribute name

        Raises
        ------
            KeyError
                if the name does not belong to the values holder.

        .. versionadded:: 0.0.1
        """
        del self._values[name]
