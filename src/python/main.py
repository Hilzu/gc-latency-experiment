import platform

if platform.python_implementation() == "CPython":
    import gc
    gc.set_debug(gc.DEBUG_STATS)

windowSize = 200000
msgCount = 1000000
msgSize = 1024

def create_message(n):
    return bytearray([n % 256] * msgSize)

def push_message(dict_, id):
    low_id = id - windowSize
    dict_[id] = create_message(id)
    if low_id >= 0:
        del dict_[low_id]

if __name__ == "__main__":
    dict_ = {}
    for i in range(msgCount):
        push_message(dict_, i)
