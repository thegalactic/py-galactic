"""
A type is associated to an :class:`Attribute <galactic.context.Attribute>`. A type is valid if it is
a class that can be called

* without argument: in that case a default value is returned for that type
* with an argument: in that case, the class try to convert it to an acceptable value for that type

For example the :class:`int` and :class:`bool` classes are acceptable types as they accept to be
called without arguments or with an argument which is converted to the desired type.
"""
