'''
Created on 19 dic 2019

@author: lorenzo
'''

import asyncio

@asyncio.coroutine
def tcp_echo_client(message, loop):
    reader, writer = yield from asyncio.open_connection('192.168.1.141', 8888, loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = yield from reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

message = 'Hello World!'
loop = asyncio.get_event_loop()

try:
    while True:
        command = input()
        if len(command) > 0:
            loop.run_until_complete(tcp_echo_client(command, loop))
finally:
    loop.close()
