

def read(address, length):
    if length < 16:
        print('Please read >= 16 bytes at once')
        return None
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

