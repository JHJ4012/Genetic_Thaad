import math
from random import randint

class Thaad:

    enemy_bullet_x = 0
    enemy_bullet_y = 0

    target_point = 0
    angle = 0

    gravity = 10
    vertical_speed = 0
    horizon_speed = 0
    first_speed = 0
    time_at_thousand = 0

    def __init__(self, target_point, angle):
        self.target_point = target_point
        self.angle = math.radians(angle)

        print('목표 지점 ', target_point)
        print('각도 ', angle)

    def calculate_Speed(self):
        self.first_speed = ( (self.gravity*self.target_point) / (2*math.sin(self.angle)*math.cos(self.angle)) )**0.5
        self.horizon_speed = self.first_speed*math.cos(self.angle)
        self.vertical_speed = self.first_speed*math.sin(self.angle)

        print('초기 속도', self.first_speed)
        print('수평 속도', thaad.horizon_speed)
        print('수직 속도', thaad.vertical_speed)

    def bullet_Location_At_Thousand(self):
        self.time_at_thousand = 1000/self.horizon_speed
        print('1000까지 가는데 시간', self.time_at_thousand)

        self.enemy_bullet_x = 1000
        self.enemy_bullet_y = (self.vertical_speed * self.time_at_thousand) - (0.5 * self.gravity * (self.time_at_thousand**2))

        print('1000에서 x좌표', self.enemy_bullet_x)
        print('1000에서 y좌표', self.enemy_bullet_y)

thaad = Thaad(randint(7000, 10000), randint(20, 70))
thaad.calculate_Speed()
thaad.bullet_Location_At_Thousand()
