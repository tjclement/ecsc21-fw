

def read(address, length):
    import esp, gc
    gc.collect()  # to explicitly clean up any previously made buffers, so we don't starve memory
    buffer = bytearray(length)
    esp.flash_raw_read(address, buffer)
    del esp
    return buffer


def _write(address, data):
    import esp, gc
    esp.flash_raw_write(address, data)
    del esp

