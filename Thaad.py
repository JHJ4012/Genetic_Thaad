import math
from random import randint

gravity = 10

#적 미사일
class Enemy:

    enemy_bullet_x_at_thousand = 0
    enemy_bullet_y_at_thousand = 0

    target_point = 0
    enemy_angle = 0

    enemy_vertical_speed = 0
    enemy_horizon_speed = 0
    enemy_first_speed = 0
    time_at_thousand = 0

    def __init__(self, target_point, enemy_angle):  # 적 미사일의 목표 지점, 적 미사일의 각도 초기화.
        self.target_point = target_point
        self.enemy_angle = math.radians(enemy_angle)

        print('적의 목표 지점 ', target_point)
        print('적 미사일 각도 ', enemy_angle)

    def calculate_Speed(self):  #받은 목표 지점과, 각도를 이용해 적 미사일의 초기 속도, 수평 속도, 수직 속도 구하고 초기화.
        self.enemy_first_speed = ( (gravity*self.target_point) / (2*math.sin(self.enemy_angle)*math.cos(self.enemy_angle)) )**0.5
        self.enemy_horizon_speed = self.enemy_first_speed*math.cos(self.enemy_angle)
        self.enemy_vertical_speed = self.enemy_first_speed*math.sin(self.enemy_angle)

        print('적 미사일 초기 속도', self.enemy_first_speed)
        print('적 미사일 수평 속도', self.enemy_horizon_speed)
        print('적 미사일 수직 속도', self.enemy_vertical_speed)

    def bullet_Location_At_Thousand(self):  # 적 미사일이 x좌표 1000까지 가는데 시간, x좌표 1000에서의 적 미사일 x,y 좌표 계산 후 초기화
        self.time_at_thousand = 1000/self.enemy_horizon_speed
        print('적 미사일이 1000까지 가는데 시간', self.time_at_thousand)

        self.enemy_bullet_x_at_thousand = 1000
        self.enemy_bullet_y_at_thousand = (self.enemy_vertical_speed * self.time_at_thousand) - (0.5 * gravity * (self.time_at_thousand**2))

        print('적 미사일 1000에서 x좌표', self.enemy_bullet_x_at_thousand)
        print('적 미사일 1000에서 y좌표', self.enemy_bullet_y_at_thousand)

#우리편 사드
class Thaad:

    found_enemy_horizon_speed = 0
    found_enemy_vertical_speed = 0

    thaad_bullet_x = 0
    thaad_bullet_y = 0

    thaad_first_speed = 0
    thaad_angle = 0
    thaad_bomb_time = 0

    thaad_horizon_speed = 0
    thaad_vertical_speed = 0

    enemy_bullet_x_for_bomb = 0
    enemy_bullet_y_for_bomb = 0
    enemy_bullet_time_for_bomb = 0

    enemy_bullet_x_rounds = 0
    enemy_bullet_y_rounds = 0
    thaad_bullet_x_rounds = 0
    thaad_bullet_y_rounds = 0

    thaad_and_enemy_distance = 0

    succeed = []

    def __init__(self, first_speed, angle, bomb_time, enemy_info):  #각종 초기화
        self.thaad_first_speed = first_speed
        self.thaad_angle = angle
        self.thaad_bomb_time = bomb_time
        self.found_enemy_horizon_speed = enemy_info.enemy_horizon_speed
        self.found_enemy_vertical_speed = enemy_info.enemy_vertical_speed
        self.enemy_bullet_time_for_bomb = enemy_info.time_at_thousand + bomb_time
        self.thaad_horizon_speed = self.thaad_first_speed * math.cos(self.thaad_angle)
        self.thaad_vertical_speed = self.thaad_first_speed * math.sin(self.thaad_angle)

        print('사드의 초기 속도', self.thaad_first_speed)
        print('사드의 각도', self.thaad_angle)
        print('사드의 터지는 시간', self.thaad_bomb_time)
        print('사드가 발견한 1000에서의 적의 수평 속도', self.found_enemy_horizon_speed)
        print('사드가 발견한 1000에서의 적의 수직 속도', self.found_enemy_vertical_speed)
        print('사드가 터질 때 적의 미사일이 날라온 시간', self.enemy_bullet_time_for_bomb)
        print('사드의 초기 수평 속도', self.thaad_horizon_speed)
        print('사드의 초기 수직 속도', self.thaad_vertical_speed)

    def bomb_Bullet_Location(self):  # 폭탄이 터지는 시점에서 사드의 x,y 좌표와 적 미사일이 x,y 좌표
        self.thaad_bullet_x = 10000 - self.thaad_horizon_speed * self.thaad_bomb_time
        self.thaad_bullet_y = (self.thaad_vertical_speed * self.thaad_bomb_time) - (0.5 * gravity * (self.thaad_bomb_time**2))

        self.enemy_bullet_x_for_bomb = self.found_enemy_horizon_speed * (self.enemy_bullet_time_for_bomb)
        self.enemy_bullet_y_for_bomb = (self.found_enemy_vertical_speed * (self.enemy_bullet_time_for_bomb)) - 0.5*gravity*(self.enemy_bullet_time_for_bomb**2)

        print('폭탄 터지는 시간에 사드의 x 좌표', self.thaad_bullet_x)
        print('폭탄 터지는 시간에 사드의 y 좌표', self.thaad_bullet_y)
        print('폭탄 터지는 시간에 적 미사일의 y 좌표', self.enemy_bullet_x_for_bomb)
        print('폭탄 터지는 시간에 적 미사일의 y 좌표', self.enemy_bullet_y_for_bomb)

        #print('폭탄 터지는 시간에 사드의 y 좌표', self.thaad_bullet_y) 이 값 왜 -나오는지 찾기.
        # -> 원인 찾음. 생각해보니 미사일이 터지기 전에 미사일이 원래 있던 지점보다 더 내려간 상태.
        # -> 만약 사드의 미사일이 터지기 전에 y좌표 0에 닿이면 자동으로 터지는 방식으로 해야겠음.
        # -> 아니면 그런 일이 일어나지 않도록 속도를 조정하는 것도 방법.
        # -> 어느 것 할지 좀 더 고민해보기.

    def succeed_Or_Failed(self):    #폭탄이 터지고 적 미사일이 그 폭팔 반경 안에 들었는지 여부 확인.

        x_distance = 0
        y_distance = 0

        #폭발 반경 : 반지름이 200인 원.
        self.thaad_bullet_x_rounds = round(self.thaad_bullet_x)
        self.thaad_bullet_y_rounds = round(self.thaad_bullet_y)
        self.enemy_bullet_x_rounds = round(self.enemy_bullet_x_for_bomb)
        self.enemy_bullet_y_rounds = round(self.enemy_bullet_y_for_bomb)

        print('반올림한 사드 x 좌표', self.thaad_bullet_x_rounds)
        print('반올림한 사드 y 좌표', self.thaad_bullet_y_rounds)
        print('반올림한 적 미사일 x 좌표', self.enemy_bullet_x_rounds)
        print('반올림한 적 미사일 y 좌표', self.enemy_bullet_y_rounds)

        x_distance = self.thaad_bullet_x_rounds - self.enemy_bullet_x_rounds
        y_distance = self.thaad_bullet_y_rounds - self.enemy_bullet_y_rounds

        if x_distance < 0:
            x_distance = x_distance * -1
        if y_distance < 0:
            y_distance = y_distance * -1

        self.thaad_and_enemy_distance = (x_distance**2 + y_distance**2)**0.5

        print('대충 사드와 미사일 사이의 거리', self.thaad_and_enemy_distance)

        if self.thaad_and_enemy_distance <= 200:
            self.succeed.append(True)
        else:
            self.succeed.append(False)

        #맞을 확률 너무 낮긴 하다. 폭팔 범위, 사드의 속도의 범위, 사드의 각도 범위를 정할 필요 있는 것 같음.
        #폭발 범위를 늘리기는 폭발 범위 너무 커야된다. 폭발 범위는 왠만하면 그대로.

#진행 시킬 컨트롤러

for i in range(20):
    enemy = Enemy(randint(7000, 10000), randint(20, 70))    # 우선 상대방은 무조건 우리 땅에 맞춰야됨. 우리 땅 면접 7000에서 10000.
                                                            # 각도는 20도에서 70도 사이.
    enemy.calculate_Speed()
    enemy.bullet_Location_At_Thousand()

    thaad = Thaad(randint(200, 500), math.radians(randint(0, 90)), randint(10, 20), enemy)   #범위 임의로 줌.
    thaad.bomb_Bullet_Location()
    thaad.succeed_Or_Failed()

print(thaad.succeed)
