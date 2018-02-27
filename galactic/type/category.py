"""
This module defines several types useful in :class:`Context` values:

* :class:`Category` created with a call to the :func:`category` function;
* :class:`ImpreciseCategory` created with a call to the :func:`imprecise_category` function
"""

from collections import OrderedDict
from typing import Iterable, Set, Iterator, Mapping, MutableMapping

from bitstring import Bits


# pylint: disable=too-few-public-methods
class ImpreciseCategory(Set[object]):
    """
    The :class:`ImpreciseCategory` class defines a generic way to create new classes over an
    imprecise category of values.

    .. versionadded:: 0.0.2
    """

    __slots__ = {'_bits'}

    _items = {}  # Mapping[object, int]
    _instances = {}  # MutableMapping[Bits, 'ImpreciseCategory']
    _cache = False  # bool

    @property
    def bits(self):
        """
        Get the bitstring representing the imprecise category.

        Returns
        -------
            :class:`Bits <bitstring:bitstring.Bits>`
                the bitstring representing the imprecise category
        """
        return self._bits

    def __new__(cls, items: Iterable[object] = None) -> 'ImpreciseCategory':
        """
        Create an :class:`ImpreciseCategory`.

        Parameters
        ----------
            items : :class:`Iterable[object] <python:collections.abc.Iterable>`
                an iterable of object

         .. versionadded:: 0.0.2
        """
        if items is None:
            bits = Bits(length=len(cls._items))
        else:
            bits = Bits([item in items for item in cls._items])
        return cls._instance(bits)

    @classmethod
    def _instance(cls, bits: Bits) -> 'ImpreciseCategory':
        """
        Create an instance or use an existing instance stored in the class cache.

        Parameters
        ----------
            bits : :class:`Bits <bitstring:bitstring.Bits>`

        Returns
        -------
            :class:`ImpreciseCategory`
                An instance of the class

        .. versionadded:: 0.0.2
        """
        if bits in cls._instances:
            return cls._instances[bits]
        else:
            instance = super().__new__(cls)
            # pylint: disable=protected-access
            instance._bits = bits
        if cls._cache:
            cls._instances[bits] = instance
        return instance

    def __contains__(self, item: object) -> bool:
        """
        Test if an item is in the category.

        Parameters
        ----------
            item : :class:`object`
                the item to test

        Returns
        -------
            :class:`bool`
                True if the item is in the category

        Raises
        ------
            ValueError
                if the item is not contained in the category class

        .. versionadded:: 0.0.2
        """

        if item in type(self)._items:
            return self._bits[type(self)._items[item]]
        else:
            raise ValueError

    def __len__(self) -> int:
        """
        Get the number of items in the category.

        Returns
        -------
            :class:`int`
                the number of items in the category

        .. versionadded:: 0.0.2
        """

        return self._bits.count(True)

    def __iter__(self) -> Iterator[object]:
        """
        Get an iterator over the items in the category.

        Returns
        -------
            :class:`Iterator[object] <python:collections.abc.Iterator>`
                an iterator

        .. versionadded:: 0.0.2
        """
        for item, index in type(self)._items.items():
            if self._bits[index]:
                yield item

    def __le__(self, other: 'ImpreciseCategory') -> bool:
        """
        Test whether every element in the imprecise category is in other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`bool`
                True if this imprecise category is included or equal to the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return not bool(self._bits & ~other.bits)
        else:
            raise TypeError

    def __lt__(self, other: 'ImpreciseCategory') -> bool:
        """
        Test whether the imprecise category is a proper subset of other, that is,
        self <= other and self != other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`bool`
                True if this imprecise category is strictely included in the other

        .. versionadded:: 0.0.2
        """
        return self <= other and self != other

    def __eq__(self, other: 'ImpreciseCategory') -> bool:
        """
        Test whether the imprecise category is equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`bool`
                True if this imprecise category is equal to the other

        .. versionadded:: 0.0.2
        """
        return not self != other

    def __ne__(self, other: 'ImpreciseCategory') -> bool:
        """
        Test whether the imprecise category is not equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`bool`
                True if this imprecise category is not equal to the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self._bits != other.bits
        else:
            raise TypeError

    def __ge__(self, other: 'ImpreciseCategory') -> bool:
        """
        Test whether every element in other is in the imprecise category.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`bool`
                True if this imprecise category includes or is equal to the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return not bool(~self._bits & other.bits)
        else:
            raise TypeError

    def __gt__(self, other: 'ImpreciseCategory') -> bool:
        """
        Test whether the imprecise category is a proper superset of other, that is,
        self >= other and self != other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`bool`
                True if this imprecise category strictely includes the other

        .. versionadded:: 0.0.2
        """
        return self >= other and self != other

    def __and__(self, other: 'ImpreciseCategory') -> 'ImpreciseCategory':
        """
        Compute the intersection between this imprecise category and the other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`ImpreciseCategory`
                the intersection between this imprecise category and the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self._instance(self._bits & other.bits)
        else:
            raise TypeError

    def __or__(self, other: 'ImpreciseCategory') -> 'ImpreciseCategory':
        """
        Compute the union between this imprecise category and the other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`ImpreciseCategory`
                the union between this imprecise category and the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self._instance(self._bits | other.bits)
        else:
            raise TypeError

    def __sub__(self, other: 'ImpreciseCategory') -> 'ImpreciseCategory':
        """
        Compute the difference between this imprecise category and the other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`ImpreciseCategory`
                the difference between this imprecise category and the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self._instance(self._bits & ~other.bits)
        else:
            raise TypeError

    def __xor__(self, other: 'ImpreciseCategory') -> 'ImpreciseCategory':
        """
        Compute the symmetric difference between this imprecise category and the other.

        Parameters
        ----------
            other : :class:`ImpreciseCategory`

        Returns
        -------
            :class:`ImpreciseCategory`
                the symmetric difference between this imprecise category and the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self._instance(self._bits ^ other.bits)
        else:
            raise TypeError

    def isdisjoint(self, other: Iterable) -> bool:
        """
        Return True if the imprecise category has no elements in common with the other.
        Imprecise categories are disjoint if and only if their intersection is the empty
        imprecise category.

        Parameters
        ----------
            other : :class:`Iterable <python:collections.abc.Iterable>`

        Returns
        -------
            :class:`bool`
                True if the imprecise category has no elements in common with other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return not bool(self._bits & other.bits)
        elif isinstance(other, Iterable):
            return self.isdisjoint(type(self)(other))
        else:
            raise TypeError

    def issubset(self, other: Iterable) -> bool:
        """
        Test whether every element in the imprecise category is in other.

        Parameters
        ----------
            other : :class:`Iterable <python:collections.abc.Iterable>`

        Returns
        -------
            :class:`bool`
                True if this imprecise category is included or equal to the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self <= other
        elif isinstance(other, Iterable):
            return self <= type(self)(other)
        else:
            raise TypeError

    def issuperset(self, other: Iterable) -> bool:
        """
        Test whether every element in other is in the imprecise category.

        Parameters
        ----------
            other : :class:`Iterable <python:collections.abc.Iterable>`

        Returns
        -------
            :class:`bool`
                True if this imprecise category includes or is equal to the other

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self >= other
        elif isinstance(other, Iterable):
            return self >= type(self)(other)
        else:
            raise TypeError

    def union(self, *others) -> 'ImpreciseCategory':
        """
        Compute the union between this imprecise category and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseCategory`
                the union between this imprecise category and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            if isinstance(other, type(self)):
                result = result | other
            else:
                result = result | type(self)(other)
        return result

    def intersection(self, *others) -> 'ImpreciseCategory':
        """
        Compute the intersection between this imprecise category and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseCategory`
                the intersection between this imprecise category and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            if isinstance(other, type(self)):
                result = result & other
            else:
                result = result & type(self)(other)
        return result

    def difference(self, *others) -> 'ImpreciseCategory':
        """
        Compute the difference between this imprecise category and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseCategory`
                the difference between this imprecise category and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            if isinstance(other, type(self)):
                result = result - other
            else:
                result = result - type(self)(other)
        return result

    def symmetric_difference(self, other: Iterable) -> 'ImpreciseCategory':
        """
        Compute the symmetric difference between this imprecise category and the others.

        Parameters
        ----------
            other : :class:`Iterable <python:collections.abc.Iterable>`

        Returns
        -------
            :class:`ImpreciseCategory`
                the symmetric difference between this imprecise category and the others

        .. versionadded:: 0.0.2
        """
        if isinstance(other, type(self)):
            return self ^ other
        elif isinstance(other, Iterable):
            return self ^ type(self)(other)
        else:
            raise TypeError

    def __repr__(self) -> str:
        """
        Convert this imprecise category to a representable string.

        Returns
        -------
            :class:`str`
                the user friendly representable string of this imprecise category

        .. versionadded:: 0.0.2
        """
        return '%s(%s)' % (type(self).__name__, str(self))

    def __str__(self) -> str:
        """
        Convert this imprecise category to a readable string.

        Returns
        -------
            :class:`str`
                the user friendly readable string of this imprecise category

        .. versionadded:: 0.0.2
        """
        return '{%s}' % (', '.join(map(repr, [item for item in self])))


def imprecise_category(name, iterable: Iterable[object] = None, **kwargs) -> type:
    """
    This function create a new dynamic class derived from the :class:`ImpreciseCategory` class.

    Example
    -------

        >>> from galactic.type.category import imprecise_category
        >>> Color = imprecise_category('Color', ['R', 'G', 'B'])

    The returned value of :func:`imprecise_category` is a class.

    Example
    -------

        >>> type(Color)
        <class 'typing.GenericMeta'>

    Its representable string is constructed using its name.

    Example
    -------

        >>> print(Color)
        __main__.Color

    A new imprecise category constructed by calling the class without argument has no possible
    values.

    Example
    -------

        >>> print(Color())
        {}
        >>> print(Color(['R']))
        {'R'}

    Element membership can be tested as for any set.

    Example
    -------

        >>> color = Color(['R', 'B'])
        >>> print(color)
        {'R', 'B'}
        >>> print('B' in color)
        True

    Elements can be iterated and it's possible to know their length.

    Example
    -------

        >>> [item for item in color]
        ['R', 'B']
        >>> print(len(color))
        2

    The class can be created in a specific module:

    Example
    -------

        >>> Color = imprecise_category('Color', ['R', 'G', 'B'], module='mymodule')
        >>> print(Color)
        mymodule.Color

    The class can cache its instances:

    Example
    -------

        >>> Color = imprecise_category('Color', ['R', 'G', 'B'], cache=True)
        >>> Color(['R', 'B']) is Color(['R', 'B'])
        True
        >>> Color = imprecise_category('Color', ['R', 'G', 'B'])
        >>> Color(['R', 'B']) is Color(['R', 'B'])
        False

    Parameters
    ----------
        name : :class:`str`
            the name of the new class
        iterable : :class:`Iterable <python:collections.abc.Iterable>`
            an iterable collection of values

    Keyword Arguments
    -----------------
        module : :class:`str`
            the module name (the current module is used if this key is not precised)
        cache : :class:`bool`
            True to cache the instances (False is the default value)

    Returns
    -------
        :class:`type <python:type>`
            a new class

    .. versionadded:: 0.0.2
    """

    if iterable is None:
        items = OrderedDict()
    else:
        items = OrderedDict.fromkeys(iterable)

    count = 0
    for item in items:
        items[item] = count
        count += 1

    if 'module' in kwargs:
        module = str(kwargs['module'])
    else:
        import inspect
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        if mod is None:
            module = '__main__'
        else:
            module = mod.__name__

    if 'cache' in kwargs:
        cache = bool(kwargs['cache'])
    else:
        cache = False

    return type(
        str(name),
        (ImpreciseCategory,),
        {
            '_items': items,
            '_instances': {},
            '_cache': bool(cache),
            '__module__': module
        }
    )


class Category(object):
    """
    The :class:`Category` class defines a generic way to create new classes over a category of
    values.
    """

    __slots__ = {'_item'}

    _items: Mapping[object, int] = {}
    _instances: MutableMapping[int, 'Category'] = {}

    def __new__(cls, value: object = None) -> 'Category':
        if not bool(cls._instances):
            for item, index in cls._items.items():
                cls._instances[index] = cls._instance(item)
        if value in cls._items:
            return cls._instances[cls._items[value]]
        elif value is None:
            return cls._instances[0]
        else:
            raise ValueError

    @classmethod
    def _instance(cls, item: object) -> 'Category':
        """
        Create an instance.

        Parameters
        ----------
            item : :class:`object <python:object>`

        Returns
        -------
            :class:`Category`
                An instance of the class

        .. versionadded:: 0.0.2
        """
        instance = super().__new__(cls)
        # pylint: disable=protected-access
        instance._item = item
        return instance

    def __str__(self) -> str:
        """
        Convert this category to a readable string.

        Returns
        -------
            :class:`str`
                the user friendly readable string of this category

        .. versionadded:: 0.0.2
        """
        return str(self._item)

    def __repr__(self) -> str:
        """
        Convert this category to a representable string.

        Returns
        -------
            :class:`str`
                the user friendly representable string of this category

        .. versionadded:: 0.0.2
        """
        return '%s(%s)' % (type(self).__name__, repr(self._item))


def category(name, iterable: Iterable[object] = None, **kwargs) -> type:
    """
    This function create a new dynamic class derived from the :class:`Category` class.

    Example
    -------

        >>> from galactic.type.category import category
        >>> Color = category('Color', ['R', 'G', 'B'])

    The returned value of :func:`category` is a class.

    Example
    -------

        >>> type(Color)
        <class 'type'>

    Its representable string is constructed using its name.

    Example
    -------

        >>> print(Color)
        <class '__main__.Color'>

    A new category constructed by calling the class without argument has the first value.

    Example
    -------

        >>> print(Color())
        R
        >>> print(Color('B'))
        B

    The class can be created in a specific module:

    Example
    -------

        >>> Color = category('Color', ['R', 'G', 'B'], module='mymodule')
        >>> print(Color)
        mymodule.Color

    Parameters
    ----------
        name : :class:`str`
            the name of the new class
        iterable : :class:`Iterable <python:collections.abc.Iterable>`
            an iterable collection of values

    Keyword arguments
    -----------------
        module : :class:`str`
            the module name (the current module is used if this key is not precised)

    Returns
    -------
        :class:`type <python:type>`
            a new class

    Raises
    ------
        ValueError
            if the iterable is empty

    .. versionadded:: 0.0.2
    """
    if iterable is None:
        items = OrderedDict()
    else:
        items = OrderedDict.fromkeys(iterable)

    if not bool(items):
        raise ValueError

    count = 0
    for item in items:
        items[item] = count
        count += 1

    if 'module' in kwargs:
        module = str(kwargs['module'])
    else:
        import inspect
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        if mod is None:
            module = '__main__'
        else:
            module = mod.__name__

    return type(
        str(name),
        (Category,),
        {
            '_items': items,
            '__module__': module
        }
    )
