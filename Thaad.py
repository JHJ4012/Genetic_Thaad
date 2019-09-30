import math
from random import randint
import numpy as np

thaad_number = 10
bullet_number = 100
gravity = 10
first_time = True

genetic_list1 = {}
genetic_list2 = {}
genetic_info = []   #유전자 리스트
score_list = []     #점수 리스트
for_evaluate_distance = []  #점수 매기기 위해 distance 넣어둘 리스트
# succeed = []
cross_over_genetic = {}
for_find_each_genetic_num = []

class Thaad:

    enemy_bullet_x_at_thousand = 0
    enemy_bullet_y_at_thousand = 0

    target_point = 0
    enemy_angle = 0

    for_enemy_angle = 0
    for_thaad_angle = 0

    enemy_vertical_speed = 0
    enemy_horizon_speed = 0
    enemy_first_speed = 0
    time_at_thousand = 0

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

    found_enemy_first_speed = 0
    found_enemy_horizon_speed = 0
    found_enemy_vertical_speed = 0

    enemy_bullet_x_rounds = 0
    enemy_bullet_y_rounds = 0
    thaad_bullet_x_rounds = 0
    thaad_bullet_y_rounds = 0

    thaad_and_enemy_distance = 0

    def __init__(self, target_point, enemy_angle):  # 적 미사일의 목표 지점, 적 미사일의 각도 초기화.
        self.target_point = target_point
        self.for_enemy_angle = enemy_angle
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
    #
    # def bullet_Location_At_Thousand(self):  # 적 미사일이 x좌표 1000까지 가는데 시간, x좌표 1000에서의 적 미사일 x,y 좌표 계산 후 초기화
    #     self.time_at_thousand = 1000/self.enemy_horizon_speed
    #     # print('적 미사일이 1000까지 가는데 시간', self.time_at_thousand)
    #
    #     self.enemy_bullet_x_at_thousand = 1000
    #     self.enemy_bullet_y_at_thousand = (self.enemy_vertical_speed * self.time_at_thousand) - (0.5 * gravity * (self.time_at_thousand**2))

        # print('적 미사일 1000에서 x좌표', self.enemy_bullet_x_at_thousand)
        # print('적 미사일 1000에서 y좌표', self.enemy_bullet_y_at_thousand)


    def shoot_Thaad(self):
        self.found_enemy_first_speed = round(self.enemy_first_speed)
        self.found_enemy_horizon_speed = round(self.enemy_horizon_speed)
        self.found_enemy_vertical_speed = round(self.enemy_vertical_speed)

        if first_time:
            self.thaad_first_speed = randint(200, 500)
            self.for_thaad_angle = randint(20, 70)
            self.thaad_angle = math.radians(self.for_thaad_angle)
            self.thaad_bomb_time = randint(10, 20)
        else:
            value = str(self.found_enemy_first_speed ) + ',' + str(self.for_enemy_angle)
            if value in cross_over_genetic:
                str2 = cross_over_genetic[value]
                arr = str2.split(',')
                self.thaad_first_speed = int(arr[0])
                self.for_thaad_angle = int(arr[1])
                self.thaad_angle = math.radians(self.for_thaad_angle)
                self.thaad_bomb_time = int(arr[2])
                # print('같다!!!!', value, self.thaad_first_speed,self.thaad_angle,self.thaad_bomb_time)
            else:
                self.thaad_first_speed = randint(200, 500)
                self.for_thaad_angle = randint(20, 70)
                self.thaad_angle = math.radians(self.for_thaad_angle)
                self.thaad_bomb_time = randint(10, 20)

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

        # if self.thaad_and_enemy_distance <= 200:
        #     succeed.append(True)
        # else:
        #     succeed.append(False)

        for_evaluate_distance.append(self.thaad_and_enemy_distance) # 점수 매기기 위해서 거리를 리스트에 넣어둠

        # print('거리 리스트에 넣기', for_evaluate_distance)
        #맞을 확률 너무 낮긴 하다. 폭팔 범위, 사드의 속도의 범위, 사드의 각도 범위를 정할 필요 있는 것 같음.
        #폭발 범위를 늘리기는 폭발 범위 너무 커야된다. 폭발 범위는 왠만하면 그대로.
        #일단 교배 시키고 진행 시키다가 조절하기. 교배하다보면 우수한 유전자로 나중에는 확률이 많이 올라갈 수도 있음.

    def store_All_Genetics(self):           #유전자 정보를 저장.
        for_store_enemy = str(self.found_enemy_first_speed) + ',' +str(self.for_enemy_angle)
        for_store_thaad = str(self.thaad_first_speed) + ',' + str(self.for_thaad_angle) + ',' + str(self.thaad_bomb_time)
        for_store_boths_info = for_store_enemy + ',' + for_store_thaad
        genetic_info.append(for_store_boths_info)
        # genetic_info 안에는 '적 수평 속도, 적 수직 속도, 사드 초기 속도, 사드 각도, 사드 폭탄 시간' 이렇게 저장됨.
        # 이 부분에서 다른 방법이 있을거임.
        # print('유전자 정보', genetic_info)

    def give_Score(self):
        # global score    # 전역 변수를 수정하기 위해 global 붙여줌
        sum_score = 0
        for i in range(len(for_evaluate_distance)):
            # # 10m에 0.1점 씩 차감. 0m일 때가 100점.
            # score = 100
            # for_calculate = (for_evaluate_distance[i]/10) * 0.1     #점수를 한 발당 점수로 하지 말고 총 합해서 한 사드당 점수를 할 것 고려해보기
            # score -= for_calculate
            # sum_score += score

            score = 0
            # print(for_evaluate_distance[i])
            if for_evaluate_distance[i] <= 600:
                score += 10000
                for_calculate = int(10000-for_evaluate_distance[i]) * 0.01
                score += for_calculate
                sum_score += score
            else:
                for_calculate = int(10000-for_evaluate_distance[i]) * 0.01
                score += for_calculate
                sum_score += score
        #     print('각 점수', score)
        # print('점수 합계들', sum_score)
        # average_score = sum_score/bullet_number
        score_list.append(sum_score)        # 각 사드의 평균 점수의 값이 들어간다



    def store_Former_Genetic(self):
        for i in range(len(cross_over_genetic)):
            cross_over_key = format(list(cross_over_genetic.keys())[i])
            cross_over_value = format(list(cross_over_genetic.values())[i])
            cross_over_key_value = cross_over_key + ',' + cross_over_value
            genetic_info.append(cross_over_key_value)
        for_find_each_genetic_num.append(len(genetic_info))

    def select_Good_Genetic(self):
        copy_score_list = []
        for i in range(len(score_list)):
            copy_score_list.append(score_list[i])
        copy_score_list.sort()

        self.good_genetic_index1 = score_list.index(copy_score_list[-1])
        self.good_genetic_index2 = score_list.index(copy_score_list[-2])

        # print('점수 리스트', score_list)
        # print('뛰어난 유전자는', self.good_genetic_index1, self.good_genetic_index2)

        # print('우수한 유전자', self.good_genetic_index1, self.good_genetic_index2)
        # print(self.good_genetic_index1, self.good_genetic_index2)           #한 세대에서 가장 점수가 높은 것의 인덱스를 가져왔음.

    def store_Good_genetic(self):
        for_divide_genetic1 = []
        for_divide_genetic2 = []

        if first_time:
            for i in range(bullet_number*self.good_genetic_index1, bullet_number*(self.good_genetic_index1+1)):
                for_divide_genetic1.append(genetic_info[i])
            for j in range(bullet_number*self.good_genetic_index2, bullet_number*(self.good_genetic_index2+1)):
                for_divide_genetic2.append(genetic_info[j])
        else:
            if self.good_genetic_index1==0:
                for i in range(0, for_find_each_genetic_num[self.good_genetic_index1]):
                    for_divide_genetic1.append(genetic_info[i])
            else:
                for i in range(for_find_each_genetic_num[self.good_genetic_index1-1], for_find_each_genetic_num[self.good_genetic_index1]):
                    for_divide_genetic1.append(genetic_info[i])

            if self.good_genetic_index2==0:
                for i in range(0, for_find_each_genetic_num[self.good_genetic_index2]):
                    for_divide_genetic2.append(genetic_info[i])
            else:
                for i in range(for_find_each_genetic_num[self.good_genetic_index2-1], for_find_each_genetic_num[self.good_genetic_index2]):
                    for_divide_genetic2.append(genetic_info[i])
        # print(genetic_info)

        for i in range(len(for_divide_genetic1)):
            arr1 = for_divide_genetic1[i].split(',')
            genetic_list1[arr1[0] + ',' + arr1[1]] = arr1[2] + ',' + arr1[3] + ',' + arr1[4]
        for i in range(len(for_divide_genetic2)):
            arr2 = for_divide_genetic2[i].split(',')
            genetic_list2[arr2[0] + ',' + arr2[1]] = arr2[2] + ',' + arr2[3] + ',' + arr2[4]
        # print('뛰어난 유전자 1',genetic_list1.keys())
        # print('뛰어난 유전자 2',genetic_list2.keys())
        # print('뛰어난 유전자 1', genetic_list1)
        # print('뛰어난 유전자 2', genetic_list2)
        #
        # print('뛰어난 유전자 1', genetic_list1)
        # print('뛰어난 유전자 2', genetic_list2)

    def crossOver(self):
        cross_over_genetic.clear()
        # print('유전자정보1', genetic_list1)
        # print('유전자정보2',genetic_list2)
        # length = 0
        # if len(genetic_list1) > len(genetic_list2):
        #     length = len(genetic_list1)
        # elif len(genetic_list1) < len(genetic_list2):
        #     length = len(genetic_list2)
        # else:
        #     length = len(genetic_list1)

        # for i in range(length):
            # random_for_cross = randint(1,2)
            #
            # if i >= len(genetic_list1):
            #     cross_over_genetic[format(list(genetic_list2.keys())[i])] = format(list(genetic_list2.values())[i])
            # elif i >= len(genetic_list2):
            #     cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
            # else:
            #     if random_for_cross == 2:
            #         cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
            #     else:
            #         cross_over_genetic[format(list(genetic_list2.keys())[i])] = format(list(genetic_list2.values())[i])

            # if i < len(genetic_list1) and i < len(genetic_list2) :
            #     if format(list(genetic_list1.keys())[i]) in genetic_list2:
            #         random_for_cross = randint(1,2)
            #         if random_for_cross == 1:
            #             cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
            #         else:
            #             cross_over_genetic[format(list(genetic_list2.keys())[i])] = genetic_list2[format(list(genetic_list1.keys())[i])]
            #     else:
            #         cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
            #         cross_over_genetic[format(list(genetic_list2.keys())[i])] = format(list(genetic_list2.values())[i])
            # elif i >= len(genetic_list1):
            #     cross_over_genetic[format(list(genetic_list2.keys())[i])] = format(list(genetic_list2.values())[i])
            # elif i >= len(genetic_list2):
            #     if format(list(genetic_list1.keys())[i]) in genetic_list2:
            #         random_for_cross = randint(1,2)
            #         if random_for_cross == 1:
            #             cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
            #         else:
            #             cross_over_genetic[format(list(genetic_list1.keys())[i])] = genetic_list2[format(list(genetic_list1.keys())[i])]
            #     else:
            #         cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
        print('뛰어난 유전자 길이1', len(genetic_list1))
        print('뛰어난 유전자 길이2', len(genetic_list2))
        for i in range(len(genetic_list1)):
            cross_over_genetic[format(list(genetic_list1.keys())[i])] = format(list(genetic_list1.values())[i])
        for i in range(len(genetic_list2)):
            if format(list(genetic_list2.keys())[i]) in cross_over_genetic:
                random_for_cross = randint(1,2)
                if random_for_cross == 2:
                    cross_over_genetic[format(list(genetic_list2.keys())[i])] = format(list(genetic_list2.values())[i])
            else:
                cross_over_genetic[format(list(genetic_list2.keys())[i])] = format(list(genetic_list2.values())[i])

    def mutation(self):
        for i in range(len(cross_over_genetic)):
            for_mutation = randint(1,2)
            if for_mutation == 1:
                cross_over_genetic[format(list(cross_over_genetic.keys())[i])] = str(randint(200, 500)) + ',' + str(randint(20, 70)) + ',' + str(randint(10, 20))
        # print('교배한 유전자', cross_over_genetic)

#진행 시킬 컨트롤러

for generation in range(10):
    if first_time:
        for i in range(thaad_number):
            # succeed.clear()
            # genetic_info.clear()
            for j in range(bullet_number):
                thaad = Thaad(randint(7000, 10000), randint(20, 70))    # 우선 상대방은 무조건 우리 땅에 맞춰야됨. 우리 땅 면접 7000에서 10000. # 각도는 20도에서 70도 사이.
                thaad.calculate_Speed()
                # thaad.bullet_Location_At_Thousand()

                thaad.shoot_Thaad()
                # 두번 째부터는 교배되고 돌연변이 된 것으로 진행. 만약 유전자에 없으면 랜덤
                thaad.bomb_Bullet_Location()
                thaad.succeed_Or_Failed()
                thaad.store_All_Genetics()

            thaad.give_Score()
            # succeed.clear()
            for_evaluate_distance.clear()

        thaad.select_Good_Genetic()
        thaad.store_Good_genetic()
        print(str(generation+1),"세대 : ",'점수 목록', score_list)
        score_list.clear()
        # thaad.store_Good_genetic()
        # print(genetic_list1)
        # print(genetic_list2)
        genetic_info.clear()
        # print(genetic_list1)
        # print(genetic_list2)
            # print('점수 목록', score_list)
            #
            # print('각 개체의 유전자 정보', genetic_info)
            # -> 해결. numpy로 해결. genetic_info에 그냥 200가지 정보 전부 다 genetic_lists에 넣은 다음에 이 것을 10,20의 2차원 배열로 바꿧음.

        # genetic_lists = np.array(genetic_info).reshape(thaad_number, bullet_number)   #genetic_lists는 1세대에서의 모든 사드 객체에 대한 정보 가지고 있음
        # print('유전 정보', genetic_lists)
        # print('fadsf', genetic_lists[0][1])
        first_time = False
    else:
        # print('뛰어난 유전자1', genetic_list1)
        # print('뛰어난 유전자2', genetic_list2)
        for i in range(thaad_number):
            thaad.crossOver()
            if i > thaad_number-3:
                thaad.mutation()
            # print('크로스오버정보',cross_over_genetic)
            for j in range(bullet_number):
                thaad = Thaad(randint(7000, 10000), randint(20, 70))
                thaad.calculate_Speed()
                thaad.shoot_Thaad()
                thaad.bomb_Bullet_Location()
                thaad.succeed_Or_Failed()
                thaad.store_All_Genetics()
            thaad.give_Score()
            thaad.store_Former_Genetic()
            # print('유전자 정보', genetic_info)
            # succeed.clear()
            for_evaluate_distance.clear()
        genetic_list1.clear()
        genetic_list2.clear()
        thaad.select_Good_Genetic()
        print(str(generation+1),"세대 : ",'점수 목록', score_list)
        score_list.clear()
        # print('뛰어난 것', thaad.good_genetic_index1, thaad.good_genetic_index2)
        thaad.store_Good_genetic()
        # print(genetic_list1)
        # print(genetic_list2)
        for_find_each_genetic_num.clear()
        genetic_info.clear()

# print('100번째의 뛰어난 유전자1', genetic_list1)
# print('100번째의 뛰어난 유전자2', genetic_list2)
# print('뛰어난 유전자를 만든 크로스 오버 정보',cross_over_genetic)
# cross over 된 유전자를 가지고 미사일 20개 대응.
#
# for i in range(thaad_number):
#     cross over 시킴.
#     for j in range(bullet_number):
#         적 미사일 발사
#         계산
#
#         shoot_Thaad 과정에서 생성하는거 필요 없음.
#         이 안의 for문에서는 cross over 시킨 것 하나로만 함.
#         위에서 바깥 쪽 for문으로 인해 사드 10번 생성되었는데 그거 필요 없음. 그걸 cross over가 함.

# print('유전자 정보 들어간거 전체', genetic_lists)


# 사드의 유전자 : 속도, 각도, 폭탄 시간.
# 적으로부터 받는 정보 : 초기 수직, 수평 속도


# 우수한 유전자 교배 및 돌연변이 생성
# 반복.

#점수 높은 것 두 개 뽑아 교배.
# 컨트롤러에서 for문 안에서 사드 발사시킬 때 if문으로 만약에 genetic_lists에 들어있는 정보로 상대 적 미사일이 쏜다면 그에 해당하는 사드 정보로 발사하도록 하기.

#클래스는 굳이 써야되는가??
