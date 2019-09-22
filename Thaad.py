import math
from random import randint
import numpy as np

thaad_number = 10
bullet_number = 20
gravity = 10
# score = 100

# genetic_lists = []   #각 사드의 유전자를 전부 저장할 리스트
genetic_info = []   #유전자 리스트
score_list = []     #점수 리스트
for_evaluate_distance = []  #점수 매기기 위해 distance 넣어둘 리스트
succeed = []

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

        # print('적의 목표 지점 ', target_point)
        # print('적 미사일 각도 ', enemy_angle)

    def calculate_Speed(self):  #받은 목표 지점과, 각도를 이용해 적 미사일의 초기 속도, 수평 속도, 수직 속도 구하고 초기화.
        self.enemy_first_speed = ( (gravity*self.target_point) / (2*math.sin(self.enemy_angle)*math.cos(self.enemy_angle)) )**0.5
        self.enemy_horizon_speed = self.enemy_first_speed*math.cos(self.enemy_angle)
        self.enemy_vertical_speed = self.enemy_first_speed*math.sin(self.enemy_angle)

        # print('적 미사일 초기 속도', self.enemy_first_speed)
        # print('적 미사일 수평 속도', self.enemy_horizon_speed)
        # print('적 미사일 수직 속도', self.enemy_vertical_speed)

    def bullet_Location_At_Thousand(self):  # 적 미사일이 x좌표 1000까지 가는데 시간, x좌표 1000에서의 적 미사일 x,y 좌표 계산 후 초기화
        self.time_at_thousand = 1000/self.enemy_horizon_speed
        # print('적 미사일이 1000까지 가는데 시간', self.time_at_thousand)

        self.enemy_bullet_x_at_thousand = 1000
        self.enemy_bullet_y_at_thousand = (self.enemy_vertical_speed * self.time_at_thousand) - (0.5 * gravity * (self.time_at_thousand**2))

        # print('적 미사일 1000에서 x좌표', self.enemy_bullet_x_at_thousand)
        # print('적 미사일 1000에서 y좌표', self.enemy_bullet_y_at_thousand)

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

    good_genetic_index1 = 0
    good_genetic_index2 = 0

    def __init__(self, first_speed, angle, bomb_time, enemy_info):  #각종 초기화
        self.thaad_first_speed = first_speed
        self.thaad_angle = angle
        self.thaad_bomb_time = bomb_time
        self.found_enemy_horizon_speed = round(enemy_info.enemy_horizon_speed)
        self.found_enemy_vertical_speed = round(enemy_info.enemy_vertical_speed)

        # self.enemy_bullet_time_for_bomb = enemy_info.time_at_thousand + bomb_time

        # 이게 적으로부터 가져오는 정보.  적의 초기 수직, 수평 속도
        # 여기서 뭔가 위에서 변수를 선언만 하고 그 변수에다가 enemy_info 객체를 집어넣을 수 있는 방법 있을지 고민해보기
        self.thaad_horizon_speed = self.thaad_first_speed * math.cos(self.thaad_angle)
        self.thaad_vertical_speed = self.thaad_first_speed * math.sin(self.thaad_angle)

        # print('사드의 초기 속도', self.thaad_first_speed)
        # print('사드의 각도', self.thaad_angle)
        # print('사드의 터지는 시간', self.thaad_bomb_time)
        # print('사드가 발견한 1000에서의 적의 수평 속도', self.found_enemy_horizon_speed)
        # print('사드가 발견한 1000에서의 적의 수직 속도', self.found_enemy_vertical_speed)
        # print('사드의 초기 수평 속도', self.thaad_horizon_speed)
        # print('사드의 초기 수직 속도', self.thaad_vertical_speed)

    def bomb_Bullet_Location(self):  # 폭탄이 터지는 시점에서 사드의 x,y 좌표와 적 미사일이 x,y 좌표

        self.enemy_bullet_time_for_bomb = (1000 / self.found_enemy_horizon_speed) + self.thaad_bomb_time
        # print('사드가 터질 때 적의 미사일이 날라온 시간', self.enemy_bullet_time_for_bomb)

        self.thaad_bullet_x = 10000 - self.thaad_horizon_speed * self.thaad_bomb_time
        self.thaad_bullet_y = (self.thaad_vertical_speed * self.thaad_bomb_time) - (0.5 * gravity * (self.thaad_bomb_time**2))

        self.enemy_bullet_x_for_bomb = self.found_enemy_horizon_speed * (self.enemy_bullet_time_for_bomb)
        self.enemy_bullet_y_for_bomb = (self.found_enemy_vertical_speed * (self.enemy_bullet_time_for_bomb)) - 0.5*gravity*(self.enemy_bullet_time_for_bomb**2)

        # print('폭탄 터지는 시간에 사드의 x 좌표', self.thaad_bullet_x)
        # print('폭탄 터지는 시간에 사드의 y 좌표', self.thaad_bullet_y)
        # print('폭탄 터지는 시간에 적 미사일의 y 좌표', self.enemy_bullet_x_for_bomb)
        # print('폭탄 터지는 시간에 적 미사일의 y 좌표', self.enemy_bullet_y_for_bomb)

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
        #
        # print('반올림한 사드 x 좌표', self.thaad_bullet_x_rounds)
        # print('반올림한 사드 y 좌표', self.thaad_bullet_y_rounds)
        # print('반올림한 적 미사일 x 좌표', self.enemy_bullet_x_rounds)
        # print('반올림한 적 미사일 y 좌표', self.enemy_bullet_y_rounds)

        x_distance = self.thaad_bullet_x_rounds - self.enemy_bullet_x_rounds
        y_distance = self.thaad_bullet_y_rounds - self.enemy_bullet_y_rounds

        if x_distance < 0:
            x_distance = x_distance * -1
        if y_distance < 0:
            y_distance = y_distance * -1

        self.thaad_and_enemy_distance = (x_distance**2 + y_distance**2)**0.5

        # print('대충 사드와 미사일 사이의 거리', self.thaad_and_enemy_distance)

        if self.thaad_and_enemy_distance <= 200:
            succeed.append(True)
        else:
            succeed.append(False)

        for_evaluate_distance.append(self.thaad_and_enemy_distance) # 점수 매기기 위해서 거리를 리스트에 넣어둠

        # print('거리 리스트에 넣기', for_evaluate_distance)
        #맞을 확률 너무 낮긴 하다. 폭팔 범위, 사드의 속도의 범위, 사드의 각도 범위를 정할 필요 있는 것 같음.
        #폭발 범위를 늘리기는 폭발 범위 너무 커야된다. 폭발 범위는 왠만하면 그대로.
        #일단 교배 시키고 진행 시키다가 조절하기. 교배하다보면 우수한 유전자로 나중에는 확률이 많이 올라갈 수도 있음.

    def store_Genetics(self):           #유전자 정보를 저장.
        for_store_enemy = str(self.found_enemy_horizon_speed) + ',' +str(self.found_enemy_vertical_speed)
        for_store_thaad = str(self.thaad_first_speed) + ',' + str(self.thaad_angle) + ',' + str(self.thaad_bomb_time)
        for_store_boths_info = for_store_enemy + ',' + for_store_thaad
        genetic_info.append(for_store_boths_info)
        # genetic_info 안에는 '적 수평 속도, 적 수직 속도, 사드 초기 속도, 사드 각도, 사드 폭탄 시간' 이렇게 저장됨.
        # 이 부분에서 다른 방법이 있을거임.
        # print('유전자 정보', genetic_info)

    def give_Score(self):
        # global score    # 전역 변수를 수정하기 위해 global 붙여줌
        sum_score = 0
        for i in range(len(for_evaluate_distance)):
            # 10m에 0.1점 씩 차감. 0m일 때가 100점.
            score = 100
            for_calculate = (for_evaluate_distance[i]/10) * 0.1
            score -= for_calculate
            sum_score += score
        #     print('각 점수', score)
        print('점수 합계들', sum_score)
        average_score = sum_score/bullet_number
        score_list.append(average_score)        # 각 사드의 평균 점수의 값이 들어간다

    def select_Good_Genetic(self):
        copy_score_list = []
        for i in range(len(score_list)):
            copy_score_list.append(score_list[i])
        copy_score_list.sort()

        self.good_genetic_index1 = score_list.index(copy_score_list[-1])
        self.good_genetic_index2 = score_list.index(copy_score_list[-2])

        print(self.good_genetic_index1, self.good_genetic_index2)           #한 세대에서 가장 점수가 높은 것의 인덱스를 가져왔음.

#진행 시킬 컨트롤러

for i in range(thaad_number):
    succeed.clear()     #나중에 UI 만들 때 쓸꺼임. 표시하도록.
    for_evaluate_distance.clear()
    # genetic_info.clear()            #뒤에 두니까 genetic_lists에 저장 되는 도중에 clear 되서 저장이 안 되는거 같아서 앞으로 옮김.

    for j in range(bullet_number):
        enemy = Enemy(randint(7000, 10000), randint(20, 70))    # 우선 상대방은 무조건 우리 땅에 맞춰야됨. 우리 땅 면접 7000에서 10000.
                                                                # 각도는 20도에서 70도 사이.
        enemy.calculate_Speed()
        enemy.bullet_Location_At_Thousand()

        thaad = Thaad(randint(200, 500), math.radians(randint(20, 70)), randint(10, 20), enemy)   #범위 임의로 줌.    이거 맨 처음에만 이렇게 주는 거임 if문으로 처리 해야됨.
        # 두번 째부터는 교배되고 돌연변이 된 것으로 진행. 만약 유전자에 없으면 랜덤. 이거 바꿔야됨.
        thaad.bomb_Bullet_Location()
        thaad.succeed_Or_Failed()
        thaad.store_Genetics()

    thaad.give_Score()
    print('점수 목록', score_list)

    # print('각 개체의 유전자 정보', genetic_info)     #이거 genetic_info 객체를 넣었기 때문에 안의 값이 아니고 주소 값이 들어가서 clear할 때 값 없어지고 마지막 것만 10개 들어가게 되는 것.
    # -> 해결. numpy로 해결. genetic_info에 그냥 200가지 정보 전부 다 genetic_lists에 넣은 다음에 이 것을 10,20의 2차원 배열로 바꿧음.

genetic_lists = np.array(genetic_info).reshape(thaad_number, bullet_number)   #genetic_lists는 1세대에서의 모든 사드 객체에 대한 정보 가지고 있음


thaad.select_Good_Genetic()

# print('유전자 정보 들어간거 전체', genetic_lists)


# 사드의 유전자 : 속도, 각도, 폭탄 시간.
# 적으로부터 받는 정보 : 초기 수직, 수평 속도



# 유전자 정보 저장할 배열 생성
# 점수 주기.

# 우수한 유전자 교배 및 돌연변이 생성
# 반복.

#점수 높은 것 두 개 뽑아 교배.
# 컨트롤러에서 for문 안에서 사드 발사시킬 때 if문으로 만약에 genetic_lists에 들어있는 정보로 상대 적 미사일이 쏜다면 그에 해당하는 사드 정보로 발사하도록 하기.

# 지금은 class 2개로 돌리는데 class를 합치고 메서드로 할까 고민해보기
