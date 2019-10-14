import math
from random import randint

thaad_number = 20
bullet_number = 100
gravity = 10
first_time = True

genetic_list1 = {}
genetic_list2 = {}
genetic_info = []
for_evaluate_distance = []
cost = []
cross_over_genetic = {}
for_find_each_genetic_num = []
fitness = []

class Thaad:

    enemy_angle = 0

    for_enemy_angle = 0
    for_thaad_angle = 0

    enemy_vertical_speed = 0
    enemy_horizon_speed = 0
    enemy_first_speed = 0

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

    thaad_and_enemy_distance = 0

    good_genetic_index1 = 0
    good_genetic_index2 = 0

    # __slots__ = ['enemy_angle', 'for_enemy_angle', 'for_thaad_angle', 'enemy_vertical_speed', 'enemy_horizon_speed', 'enemy_first_speed', 'thaad_bullet_x', 'thaad_bullet_y',
    #             'thaad_first_speed', 'thaad_angle', 'thaad_bomb_time', 'thaad_horizon_speed', 'thaad_vertical_speed', 'enemy_bullet_x_for_bomb', 'enemy_bullet_y_for_bomb',
    #             'enemy_bullet_time_for_bomb', 'thaad_and_enemy_distance', 'good_genetic_index1', 'good_genetic_index2']

    def set_Information(self, enemy_first_speed, enemy_angle):
        self.enemy_first_speed = enemy_first_speed
        self.for_enemy_angle = enemy_angle
        self.enemy_angle = math.radians(enemy_angle)
        self.enemy_horizon_speed = round(self.enemy_first_speed*math.cos(self.enemy_angle))
        self.enemy_vertical_speed = round(self.enemy_first_speed*math.sin(self.enemy_angle))
    def shoot_Thaad(self):
        value = ",".join([str(self.enemy_first_speed),str(self.for_enemy_angle)])
        if value in cross_over_genetic:
            str2 = cross_over_genetic[value]
            arr = str2.split(',')
            self.thaad_first_speed = int(arr[0])
            self.for_thaad_angle = int(arr[1])
            self.thaad_angle = math.radians(self.for_thaad_angle)
            self.thaad_bomb_time = int(arr[2])
        else:
            self.thaad_first_speed = randint(300, 500)
            self.for_thaad_angle = randint(30, 60)
            self.thaad_angle = math.radians(self.for_thaad_angle)
            self.thaad_bomb_time = randint(10, 20)

        self.thaad_horizon_speed = self.thaad_first_speed * math.cos(self.thaad_angle)
        self.thaad_vertical_speed = self.thaad_first_speed * math.sin(self.thaad_angle)


    def succeed_Or_Failed(self):

        self.enemy_bullet_time_for_bomb = round((1000 / self.enemy_horizon_speed)) + self.thaad_bomb_time

        self.thaad_bullet_x = round(10000 - self.thaad_horizon_speed * self.thaad_bomb_time)
        self.thaad_bullet_y = round((self.thaad_vertical_speed * self.thaad_bomb_time) - (0.5 * gravity * (self.thaad_bomb_time**2)))

        self.enemy_bullet_x_for_bomb = round(self.enemy_horizon_speed * (self.enemy_bullet_time_for_bomb))
        self.enemy_bullet_y_for_bomb = round((self.enemy_vertical_speed * self.enemy_bullet_time_for_bomb) - (0.5*gravity*(self.enemy_bullet_time_for_bomb**2)))

        x_distance = self.thaad_bullet_x - self.enemy_bullet_x_for_bomb
        y_distance = self.thaad_bullet_y - self.enemy_bullet_y_for_bomb

        if x_distance < 0:
            x_distance = x_distance * -1
        if y_distance < 0:
            y_distance = y_distance * -1

        self.thaad_and_enemy_distance = round((x_distance**2 + y_distance**2)**0.5)

        for_evaluate_distance.append(self.thaad_and_enemy_distance)

    def store_All_Genetics(self):

        for_store_boths_info = ",".join([str(self.enemy_first_speed),str(self.for_enemy_angle),str(self.thaad_first_speed), str(self.for_thaad_angle), str(self.thaad_bomb_time)])
        genetic_info.append(for_store_boths_info)

    def give_Cost(self):
        sum_cost = 0

        for i in for_evaluate_distance:
            if i <= 500:
                pass
            else:
                sum_cost += i

        cost.append(sum_cost)

    def store_Former_Genetic(self):
        for i in cross_over_genetic:
            genetic_info.append(i + ',' + cross_over_genetic[i])

        for_find_each_genetic_num.append(len(genetic_info))

    def select_Good_Genetic(self):      # 룰렛 휠 방식
        sum_fit = 0
        k = 4
        control = 0
        copy_cost_list = []
        for i in cost:
            copy_cost_list.append(i)

        copy_cost_list.sort()
        worst = copy_cost_list[-1]
        best = copy_cost_list[0]

        for i in cost:
            fit = (worst - i) + (worst - best)/(k-1)
            # print('거리',distance_all[i])
            # print('적합도',fit)
            fitness.append(fit)
            sum_fit += fit

        while True:
            random_val = randint(1, round(sum_fit))

            if control == 0:
                for i in range(len(fitness)):
                    random_val -= fitness[i]
                    if random_val <= 0:
                        self.good_genetic_index1 = i #같은게 나올 수 있음.
                        control += 1
                        break
            else:
                for i in range(len(fitness)):
                    random_val -= fitness[i]
                    if random_val <= 0:
                        self.good_genetic_index2 = i
                        break
            if self.good_genetic_index1 != self.good_genetic_index2:
                    break

    def store_Good_Genetic(self):
        if self.good_genetic_index1==0:
            for i in range(0, for_find_each_genetic_num[0]):
                arr1 = genetic_info[i].split(',')
                genetic_list1[arr1[0] + ',' + arr1[1]] = ",".join([arr1[2],arr1[3],arr1[4]])
        else:
            for i in range(for_find_each_genetic_num[self.good_genetic_index1-1], for_find_each_genetic_num[self.good_genetic_index1]):
                arr1 = genetic_info[i].split(',')
                genetic_list1[arr1[0] + ',' + arr1[1]] = ",".join([arr1[2],arr1[3],arr1[4]])

        if self.good_genetic_index2==0:
            for i in range(0, for_find_each_genetic_num[0]):
                arr2 = genetic_info[i].split(',')
                genetic_list2[arr2[0] + ',' + arr2[1]] = ",".join([arr2[2],arr2[3],arr2[4]])
        else:
            for i in range(for_find_each_genetic_num[self.good_genetic_index2-1], for_find_each_genetic_num[self.good_genetic_index2]):
                arr2 = genetic_info[i].split(',')
                genetic_list2[arr2[0] + ',' + arr2[1]] = ",".join([arr2[2],arr2[3],arr2[4]])

    def crossOver(self):
        cross_over_genetic.clear()

        for i in genetic_list1:
            cross_over_genetic[i] = genetic_list1[i]
        for i in genetic_list2:
            if i in cross_over_genetic:
                random_for_cross = randint(1,2)
                if random_for_cross == 2:
                    cross_over_genetic[i] = genetic_list2[i]
                # if count == 0:
                #     pass
                # elif count == 14:
                #     cross_over_genetic[i] = genetic_list2[i]
                # else:
                #     random_for_cross = randint(1,2)
                #     if random_for_cross == 2:
                #         cross_over_genetic[i] = genetic_list2[i]
            else:
                cross_over_genetic[i] = genetic_list2[i]

    def mutation(self):
        for i in cross_over_genetic:
            for_mutation = randint(1,10)
            if for_mutation == 1:
                cross_over_genetic[i] = ",".join([str(randint(300, 500)),str(randint(30, 60)),str(randint(10, 20))])

for generation in range(10000):
    if first_time:
        thaad = Thaad() #이렇게 하면 Thaad의 변수들이 계속해서 초기화 되기 때문에 계속해서 다른 메모리 공간에 값을 만들게 된다.
        for i in range(thaad_number):
            for j in range(bullet_number):
                thaad.set_Information(randint(282, 394), randint(30, 60))
                thaad.shoot_Thaad()
                thaad.succeed_Or_Failed()
                thaad.store_All_Genetics()

            thaad.give_Cost()
            thaad.store_Former_Genetic()
            for_evaluate_distance.clear()

        thaad.select_Good_Genetic()
        thaad.store_Good_Genetic()
        print(str(generation+1),"세대 : ",'적합도 목록', fitness)
        cost.clear()
        fitness.clear()
        for_find_each_genetic_num.clear()
        genetic_info.clear()
        first_time = False
        print('뛰어난 유전자 길이1', len(genetic_list1))
        print('뛰어난 유전자 길이2', len(genetic_list2))
    else:
        for i in range(thaad_number):
            thaad.crossOver()
            if i > thaad_number-6:
                thaad.mutation()
            for j in range(bullet_number):
                thaad.set_Information(randint(282, 394), randint(30, 60))
                thaad.shoot_Thaad()
                thaad.succeed_Or_Failed()
                thaad.store_All_Genetics()
            thaad.give_Cost()
            thaad.store_Former_Genetic()
            for_evaluate_distance.clear()
        genetic_list1.clear()
        genetic_list2.clear()
        thaad.select_Good_Genetic()
        thaad.store_Good_Genetic()
        print(str(generation+1),"세대 : ",'적합도 목록', fitness)
        cost.clear()
        fitness.clear()
        for_find_each_genetic_num.clear()
        genetic_info.clear()
        print('뛰어난 유전자 길이1', len(genetic_list1))
        print('뛰어난 유전자 길이2', len(genetic_list2))
        # print('유전자 정보',genetic_info)
        # print('뛰어난 유전자 1',thaad.good_genetic_index1)
        # print('뛰어난 유전자 2',thaad.good_genetic_index2)
        # print('뛰어난 유전자 1',genetic_list1)
        # print('뛰어난 유전자 2',genetic_list2)
# print(len(genetic_list1))
# print(len(genetic_list2))
