import threading
from Comm.EthernetComm import *
from Comm.MessageIO import *
from Comm.SerialComm import *
from Comm.driveManager import *


from Cinematic.PositionSolver import *
from Cinematic.JoinSystem import *
from Cinematic.LinearJoin import *
from Cinematic.RevoluteJoin import *
from Cinematic.robotAPI import *

import time

class app:
    def __init__(self):
        
        self.commPort = None
        self.messageIO_Mot = MessageIO()
        self.messageIO_Gant = MessageIO()
        self.messageIO_Mot.addDevice(SerialComm("COM3", 57600))  #Port vers openCR
        # self.messageIO_Gant.addDevice(SerialComm("COM2", 57600))  #Port vers Pico
        self.driveManager = DriveManager([0, 0, 0, 0], self.messageIO_Mot)
        
        self.JS = JoinSystem([RevoluteJoin(VectorSpaceAxis.Y, np.array([0, 0.1283, 0]), [-math.pi/4, 2 * math.pi-0.4], hardwareStepDistance= math.pi*2/4096)])
        self.JS.addJoin(RevoluteJoin(VectorSpaceAxis.Y, np.array([0, 0.245, 0]), [-math.pi/4, 2 * math.pi-0.4], hardwareStepDistance= math.pi*2/4096))
        self.JS.addJoin(RevoluteJoin(VectorSpaceAxis.X, np.array([0, 0.32824, 0]), [-math.pi/2-0.4, 2 * math.pi-0.4], hardwareStepDistance= math.pi*2/4096))


        self.robot = robotAPI(self.JS,[0., 0., 0.,0. ], self.driveManager)
        #self.robot.executeCommand(msg)

    def newConnection(self, conn):
        while True:
            self.commPort = EthernetComm(conn)
            self.messageIO.addDevice(self.commPort)
            while True:
                msg = self.messageIO.readMessage(1)
                if msg != None:
                    print("type:", msg.getType())
                    print("paload size: ", msg.getPayloadSize())
                    print("payload :", msg.getPayload())
                    self.robot.executeCommand(msg)

if __name__ == '__main__':
    # x = threading.Thread(target=waitForConnection, args=("127.0.0.1", 50000, 1, app(),))
    # x.start()

    commPort = None
    messageIO = MessageIO()
    messageIO.addDevice(SerialComm("COM3", 57600))  #Port vers open
    #messageIO.addDevice(SerialComm("COM2", 57600))  #Port vers Pico
    driveManager = DriveManager([0, 0, 0], messageIO)

        
    JS = JoinSystem([RevoluteJoin(VectorSpaceAxis.Y, np.array([0.0, 0.0, 0.0]), [-math.pi/2, math.pi/2], hardwareStepDistance= math.pi*2/4096)])
    JS.addJoin(RevoluteJoin(VectorSpaceAxis.X, np.array([0, 0.245, 0]), [-math.pi/4, math.pi/4], hardwareStepDistance= math.pi*2/4096))
    JS.addJoin(RevoluteJoin(VectorSpaceAxis.X, np.array([0, 0.245, 0]), [--math.pi/4, math.pi/4], hardwareStepDistance= math.pi*2/4096))

    robot = robotAPI(JS,[0., 0., 0.], driveManager)

    msg = ControlMessage(ControlMessage.SET_JOIN_POSITION, [0, 0, 0])
    robot.executeCommand(msg)
    '''
    val = 100
    while val < 4096:
        msg = ControlMessage(ControlMessage.SET_JOIN_POSITION, [val, val, val])
        robot.executeCommand(msg)
        #  val = val + 256
        time.sleep(10)
    '''

    # commPort = EthernetComm(conn)
    # messageIO.addDevice(commPort)
    # while True:
    #     msg = messageIO.readMessage(1)
    #     if msg != None:
    #         print("type:", msg.getType())
    #         print("paload size: ", msg.getPayloadSize())
    #         print("payload :", msg.getPayload())
    #         robot.executeCommand(msg)
