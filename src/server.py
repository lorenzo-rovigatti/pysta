'''
Created on 19 dic 2019

@author: lorenzo
'''

import asyncio
import lib

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

SERVER_HOSTNAME = ""
SERVER_PORT = 8888
BUFFER_SIZE = 100

    
class Server():
    def __init__(self, host, port, robot):
        self.loop = asyncio.get_event_loop()
        start_coroutine = asyncio.start_server(self.handle_echo, host, port, loop=self.loop)
        self.server = self.loop.run_until_complete(start_coroutine)
        self.robot = robot
        
    def run(self):
        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        
        # Close the server
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()
        
    @asyncio.coroutine
    def handle_echo(self, reader, writer):
        data = yield from reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))
        
        if message == "distance":
            response = "Current distance: %lf" % self.robot.distance()
        elif message == "left":
            self.robot.left()
            response = "Turning left"
        elif message == "right":
            self.robot.right()
            response = "Turning right"
        elif message == "forward":
            self.robot.forward()
            response = "Going forward"
        elif message == "reverse":
            self.robot.reverse()
            response = "Going backward"
        elif message == "stop":
            self.robot.stop()
            response = "Stopping"
        else:
            response = "Unrecognized command '%s'" % message
                
        print("Send: %r" % response)
        writer.write(response.encode())
        yield from writer.drain()
    
        print("Close the client socket")
        writer.close()


if __name__ == '__main__':
    try:
        lib.GPIO.setup(PINS["standby"], lib.GPIO.OUT)
        lib.GPIO.output(PINS["standby"], lib.GPIO.HIGH)
      
        us_servo = lib.Servo(PINS["servo"])
        us_sensor = lib.Ultrasonic_sensor(PINS["trigger"], PINS["echo"])
      
        left_motor = lib.Motor(PINS["volt_left"], PINS["ground_left"], PINS["pwm_left"])
        right_motor = lib.Motor(PINS["volt_right"], PINS["ground_right"], PINS["pwm_right"])
      
        robot = lib.Robot(left_motor, right_motor, us_servo, us_sensor)
        
        server = Server(SERVER_HOSTNAME, SERVER_PORT, robot)
        server.run()
    finally:
        lib.GPIO.cleanup()
    