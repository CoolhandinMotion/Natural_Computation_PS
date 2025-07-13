"""
This implementation for tabu search is modified from:
https://www.techconductor.com/algorithms/python/Search/Tabu_Search.php
Reference:
https://www.researchgate.net/publication/242527226_Tabu_Search_A_Tutorial
"""
"""
Copied from:
https://gist.github.com/mohanadkaleia/b7c8f4d9b7fb370c3910b37fbeab741b#file-tabu_search-py
"""


import copy
import math


def distance(point1:tuple[int,int,int], point2:tuple[int,int,int])->float:
    # each point is (index,x,y)
    return math.sqrt((point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

# TODO: this could way be imporved by a dict that takes (city1,city2) and maps to distance
"you dont calculate each distance twice!!!"
"This is only used once in the code."
def generate_neighbours(points:list[tuple[int,int,int]])->dict[int,dict[int,float]]:
    """This function geenrates a 2D distance matrix between all points
    Parameters
    ----------
    points : type
        Description of parameter `points`.
    Returns
    -------
    type
        Description of returned object.
    """
    dict_of_neighbours = {}

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if i not in dict_of_neighbours:
                dict_of_neighbours[i] = {}
                dict_of_neighbours[i][j]= distance(points[i], points[j])
            else:
                dict_of_neighbours[i][j] = distance(points[i], points[j])
                # dict_of_neighbours[i] = sorted(dict_of_neighbours[i].items(), key=lambda kv: kv[1])
            if j not in dict_of_neighbours:
                dict_of_neighbours[j] = {}
                dict_of_neighbours[j][i] = distance(points[j], points[i])
            else:
                dict_of_neighbours[j][i] = distance(points[j], points[i])
                # dict_of_neighbours[i] = sorted(dict_of_neighbours[i].items(), key=lambda kv: kv[1])


    return dict_of_neighbours


def _find_neighborhood(solution, dict_of_neighbours, n_opt=1):
    neighborhood_of_solution = []

    # Work with indices directly instead of values to avoid issues with duplicates
    for i in range(1, len(solution) - n_opt):
        idx1 = list(range(i, i + n_opt))

        for j in range(1, len(solution) - n_opt):
            idx2 = list(range(j, j + n_opt))

            # Skip if ranges overlap
            if set(idx1) & set(idx2):
                continue

            # Swap segments to generate a new neighbor
            new_solution = copy.deepcopy(solution)
            for k in range(n_opt):
                new_solution[idx1[k]], new_solution[idx2[k]] = (
                    solution[idx2[k]],
                    solution[idx1[k]],
                )

            # Calculate total distance
            total_distance = 0
            for k in range(len(new_solution) - 1):
                current_node = new_solution[k]
                next_node = new_solution[k + 1]
                total_distance += dict_of_neighbours[current_node][next_node]

            # Append cost and add to neighborhood if unique
            candidate = new_solution + [total_distance]
            if candidate not in neighborhood_of_solution:
                neighborhood_of_solution.append(candidate)

    # Sort neighbors by total cost (last item in list)
    neighborhood_of_solution.sort(key=lambda x: x[-1])
    return neighborhood_of_solution



def tabu_search(first_solution,
                distance_of_first_solution,
                dict_of_neighbours:dict[int,dict[int,float]],
                iters:int, size:int, n_opt=1):

    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution
    while count <= iters:
        neighborhood = _find_neighborhood(solution, dict_of_neighbours, n_opt=n_opt)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1
        found = False
        while found is False:
            i = 0
            first_exchange_node, second_exchange_node = [], []
            n_opt_counter = 0
            while i < len(best_solution):
                if best_solution[i] != solution[i]:
                    first_exchange_node.append(best_solution[i])
                    second_exchange_node.append(solution[i])
                    n_opt_counter += 1
                    if n_opt_counter == n_opt:
                        break
                i = i + 1

            exchange = first_exchange_node + second_exchange_node
            if first_exchange_node + second_exchange_node not in tabu_list and second_exchange_node + first_exchange_node not in tabu_list:
                tabu_list.append(exchange)
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            elif index_of_best_solution < len(neighborhood):
                best_solution = neighborhood[index_of_best_solution]
                index_of_best_solution = index_of_best_solution + 1

        while len(tabu_list) > size:
            tabu_list.pop(0)

        count = count + 1


    return best_solution_ever, best_cost