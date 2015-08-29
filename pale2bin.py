__author__ = 'Tachi'
import sys
import binascii
import struct

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    with open(sys.argv[1], 'r') as f:
        with open(sys.argv[1][:-3] + "bin", 'wb') as fw:
            lines = f.readlines()
            for l in lines:
                # Send@09:07:54.885 060001000000070000000035810DE1F9
                time_str, packet = l.split(' ')
                packet_bin = binascii.unhexlify(packet.strip(' \r\n'))
                if l[0] == 'S':
                    direction = 0
                else:
                    direction = 1
                buf = struct.pack("12sHB", time_str[5:], len(packet_bin), direction)
                fw.write(buf)
                fw.write(packet_bin)
