import random
import time
import jkrc
import math


class ArmControl:
    def __init__(self, ip, is_sleep=False, angular_speed=0.5, linear_speed = 50):
        self.is_sleep = is_sleep
        self.sleep_time = [random.randint(55, 100) / 1000 for i in range(10)] if self.is_sleep else 0
        self.robot = jkrc.RC(ip) # 实例化机械臂
        print("Connection successful.")
        distance = [0, 0, 100, 0, 0, 0]
        self.down = [-1 * i for i in distance]
        self.up = distance
        self.ABS = 0
        self.INCR= 1
        self.is_block = True
        self.angular_speed = angular_speed
        self.linear_speed = linear_speed
    
    def __enter__(self):
        self.robot.login() # 登录
        print("Login successful.")
        self.robot.power_on() # 上电
        self.robot.enable_robot() # 上使能
        return self

    def __exit__(self, *args):
        self.robot.disable_robot()
        self.robot.power_off()
        self.robot.logout()

    def stacking(self):
        self.__origin()

        pos0_joint = [0.9659887734969441, 1.7326170875907658, 1.5398041619333633
                        , 1.4399677308605605, -1.5707963267948966, 0.18059061009949623]
        self.__joint_move(pos0_joint)
        self.__place()

        for i in range(2):
            self.__linear_move(pos_linear=[0, 150, 0, 0, 0, 0])
            self.__place()

        pos3_joint_deg = [45, 120, 60, 90, -90, 0]
        pos3_joint = [math.radians(i) for i in pos3_joint_deg]
        self.__joint_move(pos3_joint)
        self.__place()
        
        for i in range(2):
            self.__linear_move(pos_linear=[0, 150, 0, 0, 0, 0])
            self.__place()

    def __joint_move(self, pos_joint):
        if self.is_sleep:
            sleep_time = random.sample(self.sleep_time, 1)[0]
            time.sleep(sleep_time)
            print("sleep time: ", sleep_time)
        else:
            print("sleep time: ", self.sleep_time)
        self.robot.joint_move(pos_joint, self.ABS, self.is_block, self.angular_speed)
        
    def __linear_move(self, pos_linear):
        if self.is_sleep:
            sleep_time = random.sample(self.sleep_time, 1)[0]
            time.sleep(sleep_time)
            print("sleep time: ", sleep_time)
        else:
            print("sleep time: ", self.sleep_time)
        self.robot.linear_move(pos_linear, self.INCR, self.is_block, self.linear_speed)

    def __origin(self):
        origin_pos = [0, 90, 0, 90, 0, 0]
        origin_pos_rad = [math.radians(i) for i in origin_pos]
        self.robot.joint_move(origin_pos_rad, self.ABS, self.is_block, self.angular_speed)

    def __place(self):
        self.robot.linear_move(self.down, self.INCR, self.is_block, self.linear_speed)
        self.robot.linear_move(self.up, self.INCR, self.is_block, self.linear_speed)
