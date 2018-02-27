"""
This module one type useful in :class:`Context` values:

* :class:`ImpreciseFloat` for representing imprecise numbers as intervals.
"""

import math


class ImpreciseFloat(object):
    """
    The :class:`ImpreciseFloat` class ca be used to represent intervals on the real line.
    """

    __slots__ = ['_inf', '_sup']

    def __init__(self, **kwargs):
        """
        Initialise an :class:`ImpreciseFloat`.

        Keyword arguments
        -----------------
            inf : :class:`float`
                the lower limit of the interval
                (default to :attr:`-math.inf <python:math.inf>`)
            sup : :class:`float`
                the upper limit of the interval
                (default to :attr:`math.inf <python:math.inf>`)

        .. versionadded:: 0.0.2
        """

        if 'inf' in kwargs:
            self._inf = float(kwargs['inf'])
        else:
            self._inf = -math.inf

        if 'sup' in kwargs:
            self._sup = float(kwargs['sup'])
        else:
            self._sup = math.inf

        if self._inf > self._sup:
            self._inf = math.inf
            self._sup = -math.inf

    @property
    def inf(self) -> float:
        """
        Get the lower limit.

        Returns
        -------
            :class:`float`
                the lower limit

        .. versionadded:: 0.0.2
        """
        return self._inf

    @property
    def sup(self) -> float:
        """
        Get the upper limit.

        Returns
        -------
            :class:`float`
                the upper limit

        .. versionadded:: 0.0.2
        """
        return self._sup

    def __le__(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float is included (or equal) to the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float is included in the other

        .. versionadded:: 0.0.2
        """
        return self._inf >= other.inf and self._sup <= other.sup

    def __lt__(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float is strictly included to the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float is strictly included in the other

        .. versionadded:: 0.0.2
        """
        return self <= other and self != other

    def __eq__(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float is equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float is equal to the other

        .. versionadded:: 0.0.2
        """
        return self._inf == other.inf and self._sup == other.sup

    def __ne__(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float is not equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float is not equal to the other

        .. versionadded:: 0.0.2
        """
        return not self == other

    def __ge__(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float includes or is equal to the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float includes or is equal to the other

        .. versionadded:: 0.0.2
        """
        return self._inf <= other.inf and self._sup >= other.sup

    def __gt__(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float strictly includes the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float strictly includes the other

        .. versionadded:: 0.0.2
        """
        return self >= other and self != other

    def __and__(self, other: 'ImpreciseFloat') -> 'ImpreciseFloat':
        """
        Compute the intersection of the the imprecise float with the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`ImpreciseFloat`
                the intersection of the the imprecise float with the other

        .. versionadded:: 0.0.2
        """
        return ImpreciseFloat(inf=max(self._inf, other.inf), sup=min(self._sup, other.sup))

    def __or__(self, other: 'ImpreciseFloat') -> 'ImpreciseFloat':
        """
        Compute the extension of the the imprecise float with the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`ImpreciseFloat`
                the extension of the the imprecise float with the other

        .. versionadded:: 0.0.2
        """
        return ImpreciseFloat(inf=min(self._inf, other.inf), sup=max(self._sup, other.sup))

    def isdisjoint(self, other: 'ImpreciseFloat') -> bool:
        """
        Return True if the imprecise float has no elements in common with the other.
        Imprecise floats are disjoint if and only if their intersection is the empty
        imprecise float.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`
                the other imprecise float

        Returns
        -------
            :class:`bool`
                True if the imprecise float is disjoint from the other

        .. versionadded:: 0.0.2
        """
        return self._sup < other.inf or self._inf > other.sup

    def issubset(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float is included (or equal) to the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`

        Returns
        -------
            :class:`bool`
                True if this imprecise float is included or equal to the other

        .. versionadded:: 0.0.2
        """
        return self <= other

    def issuperset(self, other: 'ImpreciseFloat') -> bool:
        """
        Test if the imprecise float includes (or is equal to) the other.

        Parameters
        ----------
            other : :class:`ImpreciseFloat`

        Returns
        -------
            :class:`bool`
                True if this imprecise float includes (or is equal to) the other

        .. versionadded:: 0.0.2
        """
        return self >= other

    def union(self, *others) -> 'ImpreciseFloat':
        """
        Compute the union between this imprecise float and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseFloat`
                the union between this imprecise float and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            result = result | other
        return result

    def intersection(self, *others) -> 'ImpreciseFloat':
        """
        Compute the intersection between this imprecise float and the others.

        Parameters
        ----------
            *others
                Variable length argument list

        Returns
        -------
            :class:`ImpreciseFloat`
                the intersection between this imprecise float and the others

        .. versionadded:: 0.0.2
        """
        result = self
        for other in others:
            result = result & other
        return result

    def __repr__(self) -> str:
        """
        Convert this imprecise float to a representable string.

        Returns
        -------
            :class:`str`
                the user friendly representable string of this imprecise float

        .. versionadded:: 0.0.2
        """
        return '%s(inf=%s, sup=%s)' % (type(self).__name__, repr(self._inf), repr(self._sup))

    def __str__(self) -> str:
        """
        Convert this imprecise float to a representable string.

        Returns
        -------
            :class:`str`
                the user friendly representable string of this imprecise float

        .. versionadded:: 0.0.2
        """
        return '[%s:%s]' % (repr(self._inf), repr(self._sup))
