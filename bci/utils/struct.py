import struct


def read_by_format(stream, format):
    size = struct.calcsize(format)
    return struct.unpack(format, stream.read(size))
