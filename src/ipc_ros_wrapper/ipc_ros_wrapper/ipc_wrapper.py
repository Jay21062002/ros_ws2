import os
import fcntl
import struct

# Define the ioctl commands
MY_IOCTL_SET_PARAMS = 0x408c6b01
MY_IOCTL_GET_PARAMS = 0x808c6b02

class MyParams(struct.Struct):
    def __init__(self):
        # Struct layout: uint32 instance, uint32 chan_id, uint32 msg_len, and a buffer of size 128 bytes
        super().__init__('I I I 128s')

params = MyParams()
device_path = '/dev/ipc_shm_sample'

def write_data(instance, chan_id, data):
    fd = os.open(device_path, os.O_RDWR)
    if fd < 0:
        raise Exception(f"Failed to open device {device_path}")
    
    if len(data) > 128:
        raise ValueError("Data length exceeds the maximum allowed length.")
    
    msg_len = len(data)
    buf = bytearray(128)
    buf[:msg_len] = data.encode('utf-8')
    
    packed_params = params.pack(instance, chan_id, msg_len, buf)
    try:
        fcntl.ioctl(fd, MY_IOCTL_SET_PARAMS, packed_params)
    except Exception as e:
        raise Exception(f"Failed to write data: {e}")
    finally:
        os.close(fd)

def read_data(instance, chan_id):
    fd = os.open(device_path, os.O_RDWR)
    if fd < 0:
        raise Exception(f"Failed to open device {device_path}")
    
    buf = bytearray(128)
    msg_len = 128
    packed_params = params.pack(instance, chan_id, msg_len, buf)
    
    try:
        result = fcntl.ioctl(fd, MY_IOCTL_GET_PARAMS, packed_params)
        unpacked_params = params.unpack(result)
        data = unpacked_params[3].decode('utf-8').rstrip('\x00')
        return data
    except Exception as e:
        raise Exception(f"Failed to read data: {e}")
    finally:
        os.close(fd)

