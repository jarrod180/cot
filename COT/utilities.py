#!/usr/bin/env python
#
# March 2017, Glenn F. Matthews
# Copyright (c) 2015-2017 the COT project developers.
# See the COPYRIGHT.txt file at the top-level directory of this distribution
# and at https://github.com/glennmatthews/cot/blob/master/COPYRIGHT.txt.
#
# This file is part of the Common OVF Tool (COT) project.
# It is subject to the license terms in the LICENSE.txt file found in the
# top-level directory of this distribution and at
# https://github.com/glennmatthews/cot/blob/master/LICENSE.txt. No part
# of COT, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE.txt file.
"""General-purpose utility functions for COT.

**Functions**

.. autosummary::
  :nosignatures:

  pretty_bytes
  to_string
"""

import logging
import sys

import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def pretty_bytes(byte_value, base_shift=0):
    """Pretty-print the given bytes value.

    Args:
      byte_value (float): Value
      base_shift (int): Base value of byte_value
            (0 = bytes, 1 = KiB, 2 = MiB, etc.)

    Returns:
      str: Pretty-printed byte string such as "1.00 GiB"

    Examples:
      ::

        >>> pretty_bytes(512)
        '512 B'
        >>> pretty_bytes(512, 2)
        '512 MiB'
        >>> pretty_bytes(65536, 2)
        '64 GiB'
        >>> pretty_bytes(65547)
        '64.01 KiB'
        >>> pretty_bytes(65530, 3)
        '63.99 TiB'
        >>> pretty_bytes(1023850)
        '999.9 KiB'
        >>> pretty_bytes(1024000)
        '1000 KiB'
        >>> pretty_bytes(1048575)
        '1024 KiB'
        >>> pretty_bytes(1049200)
        '1.001 MiB'
        >>> pretty_bytes(2560)
        '2.5 KiB'
        >>> pretty_bytes(.0001, 3)
        '104.9 KiB'
        >>> pretty_bytes(.01, 1)
        '10 B'
        >>> pretty_bytes(.001, 1)
        '1 B'
        >>> pretty_bytes(.0001, 1)
        '0 B'
        >>> pretty_bytes(100, -1)
        Traceback (most recent call last):
            ...
        ValueError: base_shift must not be negative
    """
    if base_shift < 0:
        raise ValueError("base_shift must not be negative")
    tags = ["B", "KiB", "MiB", "GiB", "TiB"]
    byte_value = float(byte_value)
    shift = base_shift
    while byte_value >= 1024.0:
        byte_value /= 1024.0
        shift += 1
    while byte_value < 1.0 and shift > 0:
        byte_value *= 1024.0
        shift -= 1
    # Fractions of a byte should be considered a rounding error:
    if shift == 0:
        byte_value = round(byte_value)
    return "{0:.4g} {1}".format(byte_value, tags[shift])


def to_string(obj):
    """Get string representation of an object, special-case for XML Element.

    Args:
      obj (object): Object to represent as a string.
    Returns:
      str: string representation
    Examples:
      ::

        >>> to_string("Hello")
        'Hello'
        >>> to_string(27.5)
        '27.5'
        >>> e = ET.Element('hello', attrib={'key': 'value'})
        >>> print(e)   # doctest: +ELLIPSIS
        <Element ...hello... at ...>
        >>> print(to_string(e))
        <hello key="value" />
    """
    if ET.iselement(obj):
        if sys.version_info[0] >= 3:
            return ET.tostring(obj, encoding='unicode')
        else:
            return ET.tostring(obj)
    else:
        return str(obj)


if __name__ == "__main__":   # pragma: no cover
    import doctest
    doctest.testmod()