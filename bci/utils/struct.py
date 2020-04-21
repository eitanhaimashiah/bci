import struct


def read_struct_by_format(stream, format):
    """Reads a struct, whose format string is `format`, from `stream`,
    and then unpacks it.

    Args:
        stream (IOBase): Stream we are reading from.
        format (str): Format string of the struct we are interested in.

    Returns:
        The unpacking of the appropriate struct. The result is a tuple
        even if it contains exactly one item.

    """
    size = struct.calcsize(format)
    return struct.unpack(format, stream.read(size))
