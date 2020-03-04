from Graph import Graph

"""
 ______     __  __     ______                 ______     ______     ______     ______    
/\  ___\   /\ \/\ \   /\  == \     _______   /\___  \   /\  ___\   /\  == \   /\  __ \   
\ \___  \  \ \ \_\ \  \ \  __<    /\______\  \/_/  /__  \ \  __\   \ \  __<   \ \ \/\ \  
 \/\_____\  \ \_____\  \ \_____\  \/______/    /\_____\  \ \_____\  \ \_\ \_\  \ \_____\ 
  \/_____/   \/_____/   \/_____/               \/_____/   \/_____/   \/_/ /_/   \/_____/ 
                                                                                                     
"""

if __name__ == '__main__':
    # FOR GENERATING GRAPH
    # itr = 421
    # for i in range(1, 6):
    #     print("\n\n\nGraph{}\n".format(itr))
    #     G = Graph(50)
    #     G.graph_to_file(itr)
    #     itr += 1
    #     # G.read_matrix('g'+str(i))
    #     G.show()

    file_name = 'g1' #tu deklaruje graf
    G = Graph(50)
    G.read_matrix(file_name)
    G.show()

    first_solution, distance_of_first_solution = G.generate_first_solution()
    dict_of_neighbours = G.generate_neighbours()
    G.find_2_neighborhood(first_solution)
    # def taboo_search(self, first_solution, distance_of_first_solution, size, time_max):
    best_solution, best_cost = G.taboo_search(first_solution, distance_of_first_solution, 6, 30)



