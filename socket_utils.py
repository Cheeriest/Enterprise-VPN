import struct
import socket

class SerializedSocket(object):
    def get_msg(self, s):
        count = struct.unpack('>I', self._get_block(s, 4))[0]
        return self._get_block(s, count)

    def send_msg(self, s, data):
        header = struct.pack('>I', len(data))
        self._send_block(s, header)
        self._send_block(s, data)
        
    def _get_block(self, s, count):
        if count <= 0:
            return ''
        buf = ''
        while len(buf) < count:
            recieve_amount = 0
            if count - len(buf) < MAX_BUFFER:
                recieve_amount = count - len(buf)
            else:
                recieve_amount = MAX_BUFFER
            buf2 = s.recv(recieve_amount)
            if not buf2:
                # error or just end of connection?
                if buf:
                    raise RuntimeError("underflow")
                else:
                    return ''
            buf += buf2
        return buf

    def _send_block(self, s, data):
        if data:
            s.sendall(data)