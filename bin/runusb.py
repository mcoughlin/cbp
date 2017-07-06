import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x0403, idProduct=0xfaf0)

print dev

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
#ep.write('test')

#byte_ints = [0x23, 0x02, 0x00, 0x00, 0x00, 0x21, 0x01] # Python recognises these as hex.
byte_ints = [0x53, 0x04, 0x06, 0x00, 0xA2, 0x01, 0x01, 0x00, 0x40, 0x0D, 0x03, 0x00]
byte_str = "".join(chr(n) for n in byte_ints)
ep.write(byte_str)

collected = 0
attempts = 50
while collected < attempts :
    try:
        data = dev.read(ep.bEndpointAddress,ep.wMaxPacketSize)
        collected += 1
        RxData = ''.join([chr(x) for x in data])
        print RxData
        #print data
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue
