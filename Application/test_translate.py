import unittest
from Comm.MessageIO import MessageIO
from Comm.translate import translate



class testTranslate(unittest.TestCase):
    msgIO = MessageIO()
    message = translate(msgIO)

    def test_chooseMode(self):
        for mode in range(1,6):
            fake_bt_msg = {'Mode' : mode, 'Flex': [100,100,100,100], 'IMU' : [0,0,0.75]}
            self.message.chooseMode(fake_bt_msg)
            self.assertEqual(self.message.getMode(), mode)
    
    def test_IMU_jogMode(self):
        valIMU = 0.75
        valMotor = 1
        for i in range(0,3):
            fake_bt_msg = {'Mode' : 1, 'Flex': [100,0,0,0], 'IMU' : [0,0,valIMU]}
            self.message.chooseMode(fake_bt_msg)
            self.assertEqual(self.message.getMsgMotor(0), valMotor)
            valIMU -= 0.75
            valMotor -= 1
    
    def test_flex_jogMode(self):
        valFlex = 80
        valMotor = 1
        for i in range(0,2):
            fake_bt_msg = {'Mode' : 1, 'Flex': [valFlex,0,0,0], 'IMU' : [0,0,0.75]}
            self.message.chooseMode(fake_bt_msg)
            self.assertEqual(self.message.getMsgMotor(0), valMotor)
            valFlex -= 5
            valMotor -= 1       
    
    def test_gripper_jogMode(self):

        # valFlex = 20
        # valMotor = 0
        # fake_bt_msg = {'Mode' : 1, 'Flex': [valFlex,valFlex,valFlex,valFlex], 'IMU' : [0,0,0.75]}
        # self.message.chooseMode(fake_bt_msg)
        # # print(self.message.getMsgMotor(-1))        
        # self.assertEqual(self.message.getMsgMotor(-1), valMotor)

        valFlex = 80
        valMotor = 1
        fake_bt_msg = {'Mode' : 1, 'Flex': [valFlex,valFlex,valFlex,valFlex], 'IMU' : [0,0,0.75]}
        self.message.chooseMode(fake_bt_msg)
        self.assertEqual(self.message.getMsgMotor(-1), valMotor)
        
        valMotor = 0
        fake_bt_msg = {'Mode' : 1, 'Flex': [valFlex,valFlex,valFlex,10], 'IMU' : [0,0,0.75]}
        self.message.chooseMode(fake_bt_msg)
        self.assertEqual(self.message.getMsgMotor(3), valMotor)

        fake_bt_msg = {'Mode' : 1, 'Flex': [valFlex,valFlex,10,valFlex], 'IMU' : [0,0,0.75]}
        self.message.chooseMode(fake_bt_msg)
        self.assertEqual(self.message.getMsgMotor(3), valMotor)

    
    

if __name__ == '__main__':
    unittest.main()