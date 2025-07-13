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

_distance_cache = {}

def calculate_total_distance(path, neighbor_dict):
    key = tuple(path)
    if key in _distance_cache:
        return _distance_cache[key]

    total = sum(
        neighbor_dict[path[i]][path[i + 1]]
        for i in range(len(path) - 1)
    )
    _distance_cache[key] = total
    return total



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


def _find_neighborhood(solution, neighbor_dict, n_opt=1):
    neighborhood = []
    solution_length = len(solution)

    for i in range(1, solution_length - n_opt):
        idx1 = list(range(i, i + n_opt))

        for j in range(1, solution_length - n_opt):
            idx2 = list(range(j, j + n_opt))

            if set(idx1) & set(idx2):
                continue

            new_solution = solution[:]
            for k in range(n_opt):
                new_solution[idx1[k]], new_solution[idx2[k]] = (
                    solution[idx2[k]],
                    solution[idx1[k]]
                )

            total_cost = calculate_total_distance(new_solution, neighbor_dict)
            candidate = new_solution + [total_cost]

            if candidate not in neighborhood:
                neighborhood.append(candidate)

    neighborhood.sort(key=lambda x: x[-1])
    return neighborhood


def tabu_search(
    initial_solution,
    initial_cost,
    neighbor_dict,
    iterations,
    tabu_size,
    n_opt=1
):
    solution = initial_solution
    best_solution = initial_solution
    best_cost = initial_cost
    tabu_list = []
    iteration = 0

    while iteration < iterations:
        neighborhood = _find_neighborhood(solution, neighbor_dict, n_opt=n_opt)
        move_accepted = False
        candidate_index = 0

        while not move_accepted and candidate_index < len(neighborhood):
            candidate = neighborhood[candidate_index]
            candidate_solution = candidate[:-1]
            candidate_cost = candidate[-1]

            diff_current = []
            diff_candidate = []
            for a, b in zip(solution, candidate_solution):
                if a != b:
                    diff_current.append(a)
                    diff_candidate.append(b)
                if len(diff_current) == n_opt:
                    break

            move = diff_current + diff_candidate
            reverse_move = diff_candidate + diff_current

            if move not in tabu_list and reverse_move not in tabu_list:
                tabu_list.append(move)
                solution = candidate_solution
                move_accepted = True

                if candidate_cost < best_cost:
                    best_cost = candidate_cost
                    best_solution = candidate_solution

            candidate_index += 1

        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        iteration += 1

    return best_solution, best_cost
