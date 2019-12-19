import asyncore
import asynchat
import socket
import RPi.GPIO as GPIO
import lib
import time
import logging

PINS = {
    "volt_left" : 37,
    "ground_left" : 38,
    "pwm_left" : 22,
    "volt_right" : 8,
    "ground_right" : 10,
    "pwm_right" : 12,
    "servo" : 18,
    "standby" : 40,
    "trigger" : 36,
    "echo" : 32
}


TCP_IP = ""
TCP_PORT = 6666
TCP_RATE = 8096
BUFFER_SIZE = 32

class EchoHandler(asynchat.async_chat):
    """Handles echoing messages from a single client.
    """

    # Artificially reduce buffer sizes to illustrate
    # sending and receiving partial messages.
    ac_in_buffer_size = 64
    ac_out_buffer_size = 64
    
    def __init__(self, sock):
        self.received_data = []
        self.logger = logging.getLogger('EchoHandler')
        asynchat.async_chat.__init__(self, sock)
        # Start looking for the ECHO command
        self.process_data = self._process_command
        self.set_terminator('\n')

    def collect_incoming_data(self, data):
        self.logger.debug('collect_incoming_data() -> (%d bytes)\n"""%s"""', len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        self.process_data()
    
    def _process_command(self):        
        command = ''.join(self.received_data)
        self.logger.debug('_process_command() "%s"', command)
        command_verb, command_arg = command.strip().split(' ')
        expected_data_len = int(command_arg)
        self.set_terminator(expected_data_len)
        self.process_data = self._process_message
        self.received_data = []
    
    def _process_message(self):
        """We have read the entire message to be sent back to the client"""
        to_echo = ''.join(self.received_data)
        self.logger.debug('_process_message() echoing\n"""%s"""', to_echo)
        self.push(to_echo)
        # Disconnect after sending the entire response
        # since we only want to do one thing at a time
        self.close_when_done()

    def handle_read(self):
        pass


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        self.logger = logging.getLogger('SERVER')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(BUFFER_SIZE)
        self.logger.debug('binding to {}'.format(self.socket.getsockname()))

    def handle_accept(self):
        socket, address = self.accept()
        self.logger.debug('new connection accepted')
        EchoHandler(socket)
        self.handle_close()

    def handle_close(self):
        self.close()


try:
    GPIO.setup(PINS["standby"], GPIO.OUT)
    GPIO.output(PINS["standby"], GPIO.HIGH)

    US_servo = lib.Servo(PINS["servo"])

    US_sensor = lib.US(PINS["trigger"], PINS["echo"])

    left_motor = lib.Motor(PINS["volt_left"], PINS["ground_left"], PINS["pwm_left"])
    right_motor = lib.Motor(PINS["volt_right"], PINS["ground_right"], PINS["pwm_right"])

    robot = lib.Robot(left_motor, right_motor, US_servo)

    logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)
    logging.debug('Server start')
    server = Server('', TCP_PORT)
    asyncore.loop()

finally:
    GPIO.cleanup()

