import asyncore
import asynchat
import socket
import time
import logging
import json

TCP_IP = '192.168.1.141'
TCP_PORT = 6666
TCP_RATE = 8096
BUFFER_SIZE = 32

class Client(asynchat.async_chat):
    """Sends messages to the server and receives responses.
    """

    # Artificially reduce buffer sizes to illustrate
    # sending and receiving partial messages.
    ac_in_buffer_size = 64
    ac_out_buffer_size = 64
    
    def __init__(self, host, port, message):
        self.message = message
        self.received_data = []
        self.logger = logging.getLogger('EchoClient')
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s', (host, port))
        self.connect((host, port))
        
    def handle_connect(self):
        self.logger.debug('handle_connect()')
        # Send the command
        self.push(b'ECHO %d\n' % len(self.message))
        # Send the data
        self.push_with_producer(EchoProducer(self.message, buffer_size=self.ac_out_buffer_size))
        # We expect the data to come back as-is, 
        # so set a length-based terminator
        self.set_terminator(len(self.message))
    
    def collect_incoming_data(self, data):
        """Read an incoming message from the client and put it into our outgoing queue."""
        self.logger.debug('collect_incoming_data() -> (%d)\n"""%s"""', len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            self.logger.debug('RECEIVED COPY OF MESSAGE')
        else:
            self.logger.debug('ERROR IN TRANSMISSION')
            self.logger.debug('EXPECTED "%s"', self.message)
            self.logger.debug('RECEIVED "%s"', received_message)

class EchoProducer(asynchat.simple_producer):
    logger = logging.getLogger('EchoProducer')

    def more(self):
        response = asynchat.simple_producer.more(self)
        self.logger.debug('more() -> (%s bytes)\n"""%s"""', len(response), response)
        return response

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

    msg = "daje".encode()
    client = Client(TCP_IP, TCP_PORT, msg)
    start = time.time()
    logging.debug('Starting async loop for all connections, unix time {}'.format(start))
    asyncore.loop()
    logging.debug('{}'.format(time.time() - start))

