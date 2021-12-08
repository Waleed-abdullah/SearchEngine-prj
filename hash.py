import zlib
x = b'zz'
a = 'zz'
y = bytes(a, 'utf-8')
x = zlib.crc32(x)
y = zlib.crc32(y)
print('x: ', x ,'\n y: ', y)