__author__ = 'Tachi'
import sys
import binascii
import struct
import zlib

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    with open(sys.argv[1], 'r') as f:
        with open(sys.argv[1][:-3] + "bin", 'wb') as fw:
            lines = f.readlines()
            for l in lines:
                # Recv 11:17:13.325 BC_NORMAL 0	4F00FFFFFFFF210002000000958AF004010010010440AA30BCBD639041C0D286BC
                _, time_str, packet_name, packet = l.split(' ')
                size, packet = packet.split('\t')
                packet_bin = binascii.unhexlify(packet.strip(' \r\n'))
                if packet_name.upper() in ('ZC_NORMAL', 'BC_NORMAL'):
                    if packet_bin[12:14] == "\x8D\xFA":
                        size = struct.unpack("H", packet_bin[14:16])[0]
                        sub_op = struct.unpack("I", packet_bin[8:12])[0]
                        buf = "\x00\x00" + zlib.decompress(packet_bin[16:16+size], -zlib.MAX_WBITS)
                        new_size = struct.pack("H", 12 + len(buf))  # fix xC_NORMAL size
                        packet_bin = packet_bin[:6] + new_size + packet_bin[8:12] + buf
                        print packet_name, sub_op, "compressed"
                elif packet_name.upper() in ('ZC_ABILITY_LIST', 'ZC_SKILL_LIST'):
                    if packet_bin[14:16] == "\x8D\xFA":
                        size = struct.unpack("H", packet_bin[16:18])[0]
                        buf = "\x00\x00" + zlib.decompress(packet_bin[18:18+size], -zlib.MAX_WBITS)
                        packet_bin = packet_bin[:14] + buf
                elif packet_name.upper() == 'ZC_ITEM_INVENTORY_LIST':
                    if packet_bin[12:14] == "\x8D\xFA":
                        size = struct.unpack("H", packet_bin[14:16])[0]
                        buf = "\x00\x00" + zlib.decompress(packet_bin[16:16+size], -zlib.MAX_WBITS)
                        packet_bin = packet_bin[:12] + buf
                if l[0] == 'S':
                    direction = 0
                else:
                    direction = 1
                buf = struct.pack("12sHB", time_str, len(packet_bin), direction)
                fw.write(buf)
                fw.write(packet_bin)
