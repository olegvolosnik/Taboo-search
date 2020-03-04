import random
import copy
import sys
import time

"""
 ______     __  __     ______                 ______     ______     ______     ______    
/\  ___\   /\ \/\ \   /\  == \     _______   /\___  \   /\  ___\   /\  == \   /\  __ \   
\ \___  \  \ \ \_\ \  \ \  __<    /\______\  \/_/  /__  \ \  __\   \ \  __<   \ \ \/\ \  
 \/\_____\  \ \_____\  \ \_____\  \/______/    /\_____\  \ \_____\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_____/   \/_____/               \/_____/   \/_____/   \/_/ /_/   \/_____/ 
                                                                                

4.	Dany jest graf spójny ze zbiorem wierzchołków V i zbiorem krawędzi E oraz wagami wi przypisanymi do każdej 
krawędzi. Należy znaleźć ścieżkę łączącą wszystkie wierzchołki (każdy odwiedzony min. raz) taką, aby minimalizować 
jej koszt S. S obliczany jest w taki sposób, że stanowi ona sumę wszystkich wag krawędzi licząc od tej wychodzącej 
z pierwszego wierzchołka ścieżki do wagi krawędzi wchodzącej do ostatniego wierzchołka ścieżki, w taki jednak sposób, 
że jeśli właśnie dodawana do S waga wi jest większa niż następna waga krawędzi na tej ścieżce: (tj. niż waga wi+1), 
wtedy do sumy dodajemy nie samo wi, ale jej 10-krotność (czyli 10 * wi).

Przyjąć początkowo: |V| minimum 100, deg(v) = [1, 6], wi = [1, 100]

"""


def reverse_solution(solution):
    reverse_sol = []
    for x in reversed(solution[1:]):
        reverse_sol.append(x)
    return reverse_sol


class Graph:
    def __init__(self, v_nr: int = 50):
        self.dict_of_neighbour = None
        self.nr_of_v = v_nr
        self.matrix = [[0 for i in range(v_nr)] for j in range(v_nr)]
        self.mk_matrix()
        self.dict_of_neighbours = {}

    def mk_matrix(self):
        # self.matrix = [
        #     [0, 42, 0, 65, 0],
        #     [42, 0, 75, 0, 99],
        #     [0, 75, 0, 0, 0],
        #     [65, 0, 0, 0, 0],
        #     [0, 99, 0, 0, 0]
        # ]

        for i in range(len(self.matrix)):
            for j in range(random.randint(1, 6)):
                self.matrix[i][random.randint(i, self.nr_of_v - 1)] = random.randint(1, 9)
            self.matrix[i][i] = 0

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j]:
                    self.matrix[j][i] = self.matrix[i][j]

    def read_matrix(self, file_name):
        fh = open(file_name, 'r')
        x_cord, y_cord = 0, 0
        for line in fh:
            line = line.split(' ')
            for c in line:
                if c == '\n':
                    continue
                self.matrix[x_cord][y_cord] = int(c)
                y_cord += 1
            x_cord += 1
            y_cord = 0

    def graph_to_file(self, itr):
        file_name = 'g{}'.format(str(itr))
        fh = open(file_name, "w")
        for line in self.matrix:
            for c in line:
                fh.write(str(c)+' ')
            fh.write('\n')

    def show(self):
        fh = open("graph.txt", "w")
        fh.write('#  |')
        for numbers in self.matrix:
            num = self.matrix.index(numbers)
            if num < 10:
                fh.write('0' + str(num) + ' ')
            else:
                fh.write(str(num) + ' ')
        fh.write('\n' + 3 * '-' + '|')
        for x in range(len(self.matrix)):
            fh.write('---')
        fh.write('\n')

        for line in self.matrix:
            num = self.matrix.index(line)
            if num < 10:
                fh.write('0' + str(num) + ' |')
            else:
                fh.write(str(num) + ' |')
            for c in line:
                if c == 0:
                    fh.write('   ')
                else:
                    fh.write(str(c) + ' ')
            fh.write('\n')

    def generate_neighbours(self):
        for i in range(len(self.matrix)):
            self.dict_of_neighbours[i] = []
            for j in range(len(self.matrix)):
                if self.matrix[i][j]:
                    lst = [j, self.matrix[i][j]]
                    self.dict_of_neighbours[i].append(lst)
        # print("This is dict of neighbours {}".format(self.dict_of_neighbours))
        return self.dict_of_neighbour

    def generate_super_random_first_solution(self):
        first_solution = []
        distance_of_first_solution = 0
        counter = 0
        last = 0
        while set(first_solution) != set(range(0, len(self.matrix))):
            new = random.randint(0, len(self.matrix) - 1)
            if self.matrix[last][new] != 0:
                first_solution.append(new)
                last = new

        if len(first_solution) > 3:
            distance_of_first_solution = self.distance_counter(first_solution)
            first_solution.insert(0, distance_of_first_solution)
        else:
            print("Graph has no solution path. Sorry.")
            sys.exit()
        print(("dist of 1 sol: {}".format(distance_of_first_solution)))
        return first_solution, distance_of_first_solution

    def generate_first_solution(self):
        first_solution = []
        distance_of_first_solution = 0
        i = 0
        counter = 0
        while set(first_solution) != set(range(0, len(self.matrix))):
            first_solution.append(i)
            walker = sorted([(rv, ri) for ri, rv in enumerate(self.matrix[i]) if ri not in first_solution and rv != 0])
            if walker:
                counter = 0
                i = walker[0][1]
            else:
                counter += 2
                if counter > len(first_solution):
                    print("This graph has isolated nodes. I can not build first solution. Sorry.")
                    sys.exit()
                else:
                    i = first_solution[-counter]
        if len(first_solution) > 3:
            distance_of_first_solution = self.distance_counter(first_solution)
        else:
            print("Graph has no solution path. Sorry.")
            sys.exit()
        print(("dist of 1 sol: {}".format(distance_of_first_solution)))
        return first_solution, distance_of_first_solution

    def proper_neighborhood(self, idx_x, idx_y, solution):
        # print("idx_x = {}, idx_y = {}, sol[idx_x] = {}, sol[idx_y] = {}"
        #   .format(idx_x, idx_y, solution[idx_x], solution[idx_y]))

        # if idx_x or idx_y > len(solution):
        #     return False

        if idx_x > 2:  # if solution[idx_x] > 0:
            if self.matrix[solution[idx_x - 1]][solution[idx_y]] == 0:
                return False

        if idx_x + 1 < len(solution):
            if solution[idx_x + 1] <= len(self.matrix):  # if solution[idx_x] - 1 < len(self.matrix):
                if self.matrix[solution[idx_x + 1]][solution[idx_y]] == 0:
                    return False

        if idx_y > 2:  # if solution[idx_y] > 0:
            if self.matrix[solution[idx_y - 1]][solution[idx_x]] == 0:
                return False

        if idx_y + 1 < len(solution):
            if solution[idx_y + 1] <= len(self.matrix):  # if idx_y - 1 < len(self.matrix):
                if self.matrix[solution[idx_y + 1]][solution[idx_x]] == 0:
                    return False

        return True

    def distance_counter(self, solution):
        # print("this is sol len {} and sol {}".format(len(solution),solution))
        distance = 0
        # print(solution)
        distance += self.matrix[solution[1]][solution[2]]
        # print("sum = {} ".format(self.matrix[solution[0]][solution[1]]), end='')
        pos = 1
        for k in solution[:-3]:
            # print("this is pos {} ".format(pos))
            a = self.matrix[solution[pos]][solution[pos + 1]]
            b = self.matrix[solution[pos + 1]][solution[pos + 2]]
            if a > b:
                distance += 10 * b
            else:
                distance += b
            pos += 1
        return distance

    def solution_cutter(self, solution):
        short_solution = []
        idx = 0
        while set(short_solution) != set(range(0, len(self.matrix))):
            if (idx >= len(solution)):
                distance = self.distance_counter(solution)
                solution.insert(0, distance)
                return solution
            short_solution.append(solution[idx])
            idx += 1
        distance = self.distance_counter(short_solution)
        short_solution.insert(0, distance)
        return short_solution

    def find_neighborhood(self, solution):
        neighborhood_of_solution = []
        x_counter, y_counter = 1, 1
        for x in solution[1:]:
            idx_x = x_counter
            for y in solution[1:]:
                idx_y = y_counter
                if x == y:
                    continue
                if not self.proper_neighborhood(idx_x, idx_y, solution):
                    continue
                _tmp = copy.deepcopy(solution[1:])
                # if idx_y or idx_x >= len(_tmp):
                #     print("idx_x = {}, idx_y = {}".format(idx_x, idx_y))
                _tmp[idx_x] = y
                _tmp[idx_y] = x
                distance = self.distance_counter(_tmp)
                _tmp.insert(0, distance)
                reverse_sol = reverse_solution(_tmp)

                _tmp = self.solution_cutter(_tmp[1:])
                reverse_sol = self.solution_cutter(reverse_sol[1:])

                if _tmp not in neighborhood_of_solution:
                    # print("we add _tmp")
                    neighborhood_of_solution.append(_tmp)
                if reverse_sol not in neighborhood_of_solution:
                    # print("we add reverse_sol")
                    neighborhood_of_solution.append(reverse_sol)
                y_counter += 1
            x_counter += 1
            y_counter = 1

        neighborhood_of_solution.sort(key=lambda z: z[0])
        print("this is neighborhood_of_solution:")
        for x in neighborhood_of_solution:
            print(x)
        return neighborhood_of_solution

    def find_2_neighborhood(self, solution):
        # solution[1, 2, 5, 8, 7, 4]
        # neighborhood_solution: [(7, 4) <--> (1, 2, 5, 8)]
        # "<-->" helper function to build sub-path between two parts
        neighborhood_2_of_solution = []
        for i in range(100):
            # print('hello')
            x = random.randint(5, len(solution) - 5)
            tmp_lst_1 = solution[1:x]
            tmp_lst_2 = solution[x:]
            sub_path = self.sub_path_builder(tmp_lst_1[0], tmp_lst_2[-1])
            neighbor = tmp_lst_1 + sub_path + tmp_lst_2
            reverse_neighbor = reverse_solution(neighbor)
            neighbor = self.solution_cutter(neighbor)
            reverse_neighbor = self.solution_cutter(reverse_neighbor)
            neighborhood_2_of_solution.append((neighbor, sub_path))
            neighborhood_2_of_solution.append((reverse_neighbor, sub_path))

        neighborhood_2_of_solution.sort(key=lambda z: z[0][0])
        # for x in neighborhood_2_of_solution:
        #     print(x[0])
        #     print(x[0])
        #     print()
        # print(neighborhood_2_of_solution[0])
        return neighborhood_2_of_solution

    def sub_path_builder(self, node_1, node_2):
        sub_path = []

        if self.matrix[node_1][node_2]:
            sub_path.append(node_1)
            sub_path.append(node_2)
            # print("CASE I")
        else:
            # best_min = 1000
            # for x in self.dict_of_neighbours[node_1]:
            #     for y in self.dict_of_neighbours[node_2]:
            #         print("\n\nx = {}, y = {}\n\n".format(x, y))
            #         if x == y:
            #             print("CASE II - need to fix")
            #             print(node_1, node_2, x, y)
            #             tmp_min = self.matrix[int(node_1)][int(x)] + self.matrix[int(y)][int(node_2)]
            #             if best_min > tmp_min:
            #                 best_min = tmp_min
            #                 best_xy = x
            #             tmp_min = 0
            # if best_min == 1000:
            sub_path.append(node_2)
            while node_1 not in set(sub_path):
                new = random.randint(0, len(self.matrix) - 1)
                if self.matrix[sub_path[-1]][new] != 0:
                    sub_path.append(new)
        return sub_path

    def taboo_search(self, first_solution, distance_of_first_solution, size_of_taboo_list, time_max):
        start_time = time.time()
        count = 0
        solution = first_solution
        # taboo_list = list()
        taboo_2_list = list()
        best_cost = distance_of_first_solution
        best_solution_ever = solution

        local_optimum = 0
        restarted = False
        time_limit = True
        ignore_taboo = False

        # while count < iterations:
        while time_limit:
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))
            time1 = int(time.time())
            act_time = int(time1 - start_time)
            if act_time > time_max:
                time_limit = False
                print("act_time = {}".format(act_time))

            print('this is iter: {}'.format(count))
            cost = best_solution_ever[0]
            print(cost, taboo_2_list)
            neighborhood = self.find_2_neighborhood(solution)

            index_of_best_solution = 0
            if len(neighborhood) > 1:
                best_solution = neighborhood[0]
            else:
                print("this solution has no better neighborhood.")
                print(cost, best_solution_ever)
                sys.exit()
            found = False
            while found is False:
                i = 1
                # while i < len(best_solution):
                #     if best_solution[i] != solution[i]:
                #         first_exchange_node = best_solution[i]
                #         second_exchange_node = solution[i]
                #         break
                #     i += 1
                # need find new idea for taboo list !!!
                if neighborhood[index_of_best_solution][1] not in taboo_2_list or ignore_taboo:
                    taboo_2_list.append(neighborhood[index_of_best_solution][1])
                    found = True
                    ignore_taboo = False
                    solution = best_solution[0]
                    cost = best_solution[0][0]
                    # if [first_exchange_node, second_exchange_node] not in taboo_list:
                    #     taboo_list.append([first_exchange_node, second_exchange_node])
                    #     found = True
                    #     solution = best_solution
                    #     cost = neighborhood[index_of_best_solution][0]
                    if cost < best_cost:
                        if restarted:
                            restarted = False
                        best_cost = cost
                        # print("this is iter {}, cost = {}".format(count, best_cost))
                        best_solution_ever = solution
                        local_optimum = 0
                    elif cost >= best_cost and not restarted:
                    # elif cost >= best_cost:
                        local_optimum += 1
                else:
                    print("TEST -> index of best solution += 1")
                    print(neighborhood[index_of_best_solution])
                    index_of_best_solution += 1
                    if len(neighborhood) < index_of_best_solution + 1:
                        print("TEST -> index of best solution += 1")
                        index_of_best_solution = 0
                        ignore_taboo = True
            if len(taboo_2_list) >= size_of_taboo_list:
                taboo_2_list.pop(0)
            count += 1

            if local_optimum > 10:
                solution, new_dist = self.generate_super_random_first_solution()
                print("We are in local minimum, we generate new solution with len {}, sol = {}".format(len(solution),
                                                                                                       solution))
                local_optimum = -40
                restarted = True
                taboo_2_list.clear()

        cost = best_solution_ever[0]
        print("End of taboo: {}".format(cost))
        print(cost, best_solution_ever)
        return best_solution_ever, cost
