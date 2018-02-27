"""
This module defines one type useful in :class:`Context` values:

"""

from galactic.type.category import imprecise_category

# pylint: disable=invalid-name
ImpreciseBoolean = imprecise_category('ImpreciseBoolean', [True, False], cache=True)
"""
The :class:`ImpreciseBoolean <ImpreciseCategory>` class is an imprecise category
representing the possible boolean values :code:`[True, False]`. It has been created using
the :func:`imprecise_category <galactic.type.category.imprecise_category>` function.

    >>> ImpreciseBoolean = imprecise_category('ImpreciseBoolean', [True, False], cache=True)
"""
