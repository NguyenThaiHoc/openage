# Copyright 2015-2016 the openage authors. See copying.md for legal info.
"""
Misc string helper functions; this includes encoding, decoding,
manipulation, ...
"""


def decode_until_null(data, encoding='utf-8'):
    """
    decodes a bytes object, aborting at the first \\0 character.

    >>> decode_until_null(b"foo\\0bar")
    'foo'
    """
    end = data.find(0)
    if end != -1:
        data = data[:end]

    return data.decode(encoding)


def try_decode(data):
    """
    does its best to attempt decoding the given string of unknown encoding.
    """
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        pass

    return data.decode('iso-8859-1')


def binstr(num, bits=None, group=8):
    """
    Similar to the built-in bin(), but optionally takes
    the number of bits as an argument, and prints underscores instead of
    zeroes.

    >>> binstr(1337, 16)
    '_____1_1 __111__1'
    """
    result = bin(num)[2:]

    if bits is not None:
        result = result.rjust(bits, '0')

    result = result.replace('0', '_')

    if group is not None:
        pos = 0
        grouped = []
        while pos < len(result):
            grouped.append(result[pos:pos + group])
            pos += group
        result = ' '.join(grouped)

    return result


def colorize(string, colorcode):
    """
    Colorizes string with the given EMCA-48 SGR code.

    >>> colorize('foo', '31;1')
    '\\x1b[31;1mfoo\\x1b[m'
    """
    if colorcode:
        return '\x1b[' + colorcode + 'm' + str(string) + '\x1b[m'
    else:
        return str(string)


def lstrip_once(string, substr):
    """
    Removes substr at the left of string, and raises ValueError on failure.

    >>> lstrip_once("openage.test", "openage.")
    'test'
    >>> lstrip_once("libopenage.test", "openage.")
    Traceback (most recent call last):
    ValueError: 'libopenage.test' doesn't start with 'openage.'
    """
    if not string.startswith(substr):
        raise ValueError("%s doesn't start with %s" %
                         (repr(string), repr(substr)))

    return string[len(substr):]


def rstrip_once(string, substr):
    """
    Removes substr at the right of string, and raises ValueError on failure.

    >>> rstrip_once("test.cpp", ".cpp")
    'test'
    """
    if not string.endswith(substr):
        raise ValueError("%s doesn't end with %s" %
                         (repr(string), repr(substr)))

    return string[:-len(substr)]


def format_progress(progress, total):
    """
    Formats an "x out of y" string with fixed width.

    >>> format_progress(5, 20)
    ' 5/20'
    """
    return "%*d/%d" % (len(str(total)), progress, total)
