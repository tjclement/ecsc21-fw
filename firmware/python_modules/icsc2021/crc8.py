#                          The MIT License (MIT)
#
#                     Copyright (c) 2016 Nicco Kunzmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""The crc8 module.

The crc8 module provides the same interface as the hashlib module.
    https://docs.python.org/2/library/hashlib.html

Some code was copied from here:
    https://dzone.com/articles/crc8py
and gave credit "From the PyPy project" and the link
    http://snippets.dzone.com/posts/show/3543

"""
import sys

__author__ = "Nicco Kunzmann"
__version__ = "0.1.0"


class crc8(object):
    digest_size = 1
    block_size = 1

    _table = [
        0x00,
        0x07,
        0x0E,
        0x09,
        0x1C,
        0x1B,
        0x12,
        0x15,
        0x38,
        0x3F,
        0x36,
        0x31,
        0x24,
        0x23,
        0x2A,
        0x2D,
        0x70,
        0x77,
        0x7E,
        0x79,
        0x6C,
        0x6B,
        0x62,
        0x65,
        0x48,
        0x4F,
        0x46,
        0x41,
        0x54,
        0x53,
        0x5A,
        0x5D,
        0xE0,
        0xE7,
        0xEE,
        0xE9,
        0xFC,
        0xFB,
        0xF2,
        0xF5,
        0xD8,
        0xDF,
        0xD6,
        0xD1,
        0xC4,
        0xC3,
        0xCA,
        0xCD,
        0x90,
        0x97,
        0x9E,
        0x99,
        0x8C,
        0x8B,
        0x82,
        0x85,
        0xA8,
        0xAF,
        0xA6,
        0xA1,
        0xB4,
        0xB3,
        0xBA,
        0xBD,
        0xC7,
        0xC0,
        0xC9,
        0xCE,
        0xDB,
        0xDC,
        0xD5,
        0xD2,
        0xFF,
        0xF8,
        0xF1,
        0xF6,
        0xE3,
        0xE4,
        0xED,
        0xEA,
        0xB7,
        0xB0,
        0xB9,
        0xBE,
        0xAB,
        0xAC,
        0xA5,
        0xA2,
        0x8F,
        0x88,
        0x81,
        0x86,
        0x93,
        0x94,
        0x9D,
        0x9A,
        0x27,
        0x20,
        0x29,
        0x2E,
        0x3B,
        0x3C,
        0x35,
        0x32,
        0x1F,
        0x18,
        0x11,
        0x16,
        0x03,
        0x04,
        0x0D,
        0x0A,
        0x57,
        0x50,
        0x59,
        0x5E,
        0x4B,
        0x4C,
        0x45,
        0x42,
        0x6F,
        0x68,
        0x61,
        0x66,
        0x73,
        0x74,
        0x7D,
        0x7A,
        0x89,
        0x8E,
        0x87,
        0x80,
        0x95,
        0x92,
        0x9B,
        0x9C,
        0xB1,
        0xB6,
        0xBF,
        0xB8,
        0xAD,
        0xAA,
        0xA3,
        0xA4,
        0xF9,
        0xFE,
        0xF7,
        0xF0,
        0xE5,
        0xE2,
        0xEB,
        0xEC,
        0xC1,
        0xC6,
        0xCF,
        0xC8,
        0xDD,
        0xDA,
        0xD3,
        0xD4,
        0x69,
        0x6E,
        0x67,
        0x60,
        0x75,
        0x72,
        0x7B,
        0x7C,
        0x51,
        0x56,
        0x5F,
        0x58,
        0x4D,
        0x4A,
        0x43,
        0x44,
        0x19,
        0x1E,
        0x17,
        0x10,
        0x05,
        0x02,
        0x0B,
        0x0C,
        0x21,
        0x26,
        0x2F,
        0x28,
        0x3D,
        0x3A,
        0x33,
        0x34,
        0x4E,
        0x49,
        0x40,
        0x47,
        0x52,
        0x55,
        0x5C,
        0x5B,
        0x76,
        0x71,
        0x78,
        0x7F,
        0x6A,
        0x6D,
        0x64,
        0x63,
        0x3E,
        0x39,
        0x30,
        0x37,
        0x22,
        0x25,
        0x2C,
        0x2B,
        0x06,
        0x01,
        0x08,
        0x0F,
        0x1A,
        0x1D,
        0x14,
        0x13,
        0xAE,
        0xA9,
        0xA0,
        0xA7,
        0xB2,
        0xB5,
        0xBC,
        0xBB,
        0x96,
        0x91,
        0x98,
        0x9F,
        0x8A,
        0x8D,
        0x84,
        0x83,
        0xDE,
        0xD9,
        0xD0,
        0xD7,
        0xC2,
        0xC5,
        0xCC,
        0xCB,
        0xE6,
        0xE1,
        0xE8,
        0xEF,
        0xFA,
        0xFD,
        0xF4,
        0xF3,
    ]

    def __init__(self, initial_string=b"", initial_start=0x00):
        """Create a new crc8 hash instance."""
        self._sum = initial_start
        self._update(initial_string)

    def update(self, bytes_):
        """Update the hash object with the string arg.

        Repeated calls are equivalent to a single call with the concatenation
        of all the arguments: m.update(a); m.update(b) is equivalent
        to m.update(a+b).
        """
        self._update(bytes_)

    def digest(self):
        """Return the digest of the bytes passed to the update() method so far.

        This is a string of digest_size bytes which may contain non-ASCII
        characters, including null bytes.
        """
        return self._digest()

    def hexdigest(self):
        """Return digest() as hexadecimal string.

        Like digest() except the digest is returned as a string of double
        length, containing only hexadecimal digits. This may be used to
        exchange the value safely in email or other non-binary environments.
        """
        return hex(self._sum)[2:].zfill(2)

    def _update(self, bytes_):
        if isinstance(bytes_, str):
            raise TypeError("Unicode-objects must be encoded before hashing")
        elif not isinstance(bytes_, (bytes, bytearray)):
            raise TypeError("object supporting the buffer API required")
        table = self._table
        _sum = self._sum
        for byte in bytes_:
            _sum = table[_sum ^ byte]
        self._sum = _sum

    def _digest(self):
        return bytes([self._sum])

    def copy(self):
        """Return a copy ("clone") of the hash object.

        This can be used to efficiently compute the digests of strings that
        share a common initial substring.
        """
        crc = crc8()
        crc._sum = self._sum
        return crc


__all__ = ["crc8"]
