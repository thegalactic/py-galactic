"""
This module one type useful in :class:`Context` values:

* :class:`ImpreciseFloat` for representing imprecise float as intervals.
* :class:`ImpreciseInteger` for representing imprecise int as intervals.
"""

import math
import sys
from abc import abstractmethod
from typing import TypeVar, Generic

N = TypeVar('N', float, int)


class ImpreciseNumber(Generic[N]):
    """
    The :class:`ImpreciseNumber` class ca be used to represent intervals.

    .. versionadded:: 0.0.3
    """

    @classmethod
    @abstractmethod
    def default_lower(cls):
        """
        Get the default lower limit for that class.

        Returns
        -------
            :class:`N`
                The default lower limit

        .. versionadded:: 0.0.3
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def default_upper(cls):
        """
        Get the default upper limit for that class.

        Returns
        -------
            :class:`N`
                The default upper limit

        .. versionadded:: 0.0.3
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def convert(cls, value):
        """
        Convert the value to the desired type.

        Parameters
        ----------
            value
                Value to be converted

        Returns
        -------
            :class:`N`
                The default lower limit

        .. versionadded:: 0.0.3
        """
        raise NotImplementedError

    def __init__(self, **kwargs):
        """
        Initialise an :class:`ImpreciseNumber`.

        Keyword arguments
        -----------------
            lower : :class:`N`
                the lower limit of the interval
            upper : :class:`N`
                the upper limit of the interval

        .. versionadded:: 0.0.2
        """

        if 'lower' in kwargs:
            self._lower = self.convert(kwargs['lower'])
        else:
            self._lower = self.default_lower()

        if 'upper' in kwargs:
            self._upper = self.convert(kwargs['upper'])
        else:
            self._upper = self.default_upper()

        if self._lower > self._upper:
            self._lower = self.default_upper()
            self._upper = self.default_lower()

    @property
    def lower(self):
        """
        Get the lower limit.

        Returns
        -------
            :class:`N`
                the lower limit

        .. versionadded:: 0.0.2
        """
        return self._lower

    @property
    def upper(self):
        """
        Get the upper limit.

        Returns
        -------
            :class:`N`
                the upper limit

        .. versionadded:: 0.0.2
        """
        return self._upper

    def __le__(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Test if the imprecise number is included (or equal) to the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number is included in the other

        .. versionadded:: 0.0.2
        """
        return self._lower >= other.lower and self._upper <= other.upper

    def __lt__(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Test if the imprecise number is strictly included to the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number is strictly included in the other

        .. versionadded:: 0.0.2
        """
        return self <= other and self != other

    def __eq__(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Test if the imprecise number is equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number is equal to the other

        .. versionadded:: 0.0.2
        """
        return self._lower == other.lower and self._upper == other.upper

    def __ne__(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Test if the imprecise number is not equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number is not equal to the other

        .. versionadded:: 0.0.2
        """
        return not self == other

    def __ge__(self, other: N) -> bool:
        """
        Test if the imprecise number includes or is equal to the other.

        Parameters
        ----------
            other : :class:`N`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number includes or is equal to the other

        .. versionadded:: 0.0.2
        """
        return self._lower <= other.lower and self._upper >= other.upper

    def __gt__(self, other: N) -> bool:
        """
        Test if the imprecise number strictly includes the other.

        Parameters
        ----------
            other : :class:`N`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number strictly includes the other

        .. versionadded:: 0.0.2
        """
        return self >= other and self != other

    def __and__(self, other: 'ImpreciseNumber[N]') -> 'ImpreciseNumber[N]':
        """
        Compute the intersection of the the imprecise number with the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`ImpreciseNumber[N]`
                the intersection of the the imprecise number with the other

        .. versionadded:: 0.0.2
        """
        return type(self)(lower=max(self._lower, other.lower), upper=min(self._upper, other.upper))

    def __or__(self, other: 'ImpreciseNumber[N]') -> 'ImpreciseNumber[N]':
        """
        Compute the extension of the the imprecise number with the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`ImpreciseNumber[N]`
                the extension of the the imprecise number with the other

        .. versionadded:: 0.0.2
        """
        return type(self)(lower=min(self._lower, other.lower), upper=max(self._upper, other.upper))

    def isdisjoint(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Return True if the imprecise number has no elements in common with the other.
        Imprecise numbers are disjoint if and only if their intersection is the empty
        imprecise number.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`
                the other imprecise number

        Returns
        -------
            :class:`bool`
                True if the imprecise number is disjoint from the other

        .. versionadded:: 0.0.2
        """
        return self._upper < other.lower or self._lower > other.upper

    def issubset(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Test if the imprecise number is included (or equal) to the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`

        Returns
        -------
            :class:`bool`
                True if this imprecise number is included or equal to the other

        .. versionadded:: 0.0.2
        """
        return self <= other

    def issuperset(self, other: 'ImpreciseNumber[N]') -> bool:
        """
        Test if the imprecise number includes (or is equal to) the other.

        Parameters
        ----------
            other : :class:`ImpreciseNumber[N]`

        Returns
        -------
            :class:`bool`
                True if this imprecise number includes (or is equal to) the other

        .. versionadded:: 0.0.2
        """
        return self >= other

    def union(self, *others) -> 'ImpreciseNumber[N]':
        """
        Compute the union between this imprecise number and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseNumber[N]`
                the union between this imprecise number and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            result = result | other
        return result

    def intersection(self, *others) -> 'ImpreciseNumber[N]':
        """
        Compute the intersection between this imprecise number and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseNumber[N]`
                the intersection between this imprecise number and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            result = result & other
        return result

    def __repr__(self) -> str:
        """
        Convert this imprecise number to a representable string.

        Returns
        -------
            :class:`str`
                the user friendly representable string of this imprecise number

        .. versionadded:: 0.0.2
        """
        return '%s(lower=%s, upper=%s)' %\
               (type(self).__name__, repr(self._lower), repr(self._upper))

    def __str__(self) -> str:
        """
        Convert this imprecise number to a representable string.

        Returns
        -------
            :class:`str`
                the user friendly representable string of this imprecise number

        .. versionadded:: 0.0.2
        """
        return '[%s:%s]' % (repr(self._lower), repr(self._upper))


class ImpreciseFloat(ImpreciseNumber[float]):
    """
    :class:`ImpreciseFloat` instances represents subset of the real line.

    .. versionadded:: 0.0.2
    """

    @classmethod
    def convert(cls, value):
        """
        Convert the value to a float.

        Parameters
        ----------
            value
                The value to convert

        Returns
        -------
            :class:`float`
                The value converted

        .. versionadded:: 0.0.3
        """
        return float(value)

    @classmethod
    def default_lower(cls):
        """
        Get the default lower limit for that class.

        Returns
        -------
            :class:`float`
                The default lower limit is fixed to :code:`-math.inf`

        .. versionadded:: 0.0.3
        """
        return -math.inf

    @classmethod
    def default_upper(cls):
        """
        Get the default upper limit for that class.

        Returns
        -------
            :class:`float`
                The default upper limit is fixed to :code:`math.inf`

        .. versionadded:: 0.0.3
        """
        return math.inf


class ImpreciseInteger(ImpreciseNumber[int]):
    """
    :class:`ImpreciseInteger` instances represents subset of the integer set.

    .. versionadded:: 0.0.3
    """

    @classmethod
    def convert(cls, value):
        """
        Convert the value to an int.

        Parameters
        ----------
            value
                The value to convert

        Returns
        -------
            :class:`int`
                The value converted

        .. versionadded:: 0.0.3
        """
        return int(value)

    @classmethod
    def default_lower(cls):
        """
        Get the default lower limit for that class.

        Returns
        -------
            :class:`int`
                The default lower limit is fixed to :code:`-sys.maxsize`

        .. versionadded:: 0.0.3
        """
        return -sys.maxsize

    @classmethod
    def default_upper(cls):
        """
        Get the default upper limit for that class.

        Returns
        -------
            :class:`int`
                The default upper limit is fixed to :code:`sys.maxsize`

        .. versionadded:: 0.0.3
        """
        return sys.maxsize
