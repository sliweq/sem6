from dijkstra_and_a import (
    Stop,
    load_data,
    remove_duplicates,
    process_data,
    time_to_seconds,
    seconds_to_time,
)
from sys import maxsize as infinity
from typing import Dict, Tuple
from tabu_algorithms import a_star
import random
from queue import Queue
import time
import sys
import math


def calculate_cost(
    stops: list[str], time_on_stop: int, data: Dict[str, Stop], opt_time: bool = True
) -> int:
    last_line = None
    for i in range(len(stops) - 1):
        a_star_solution = a_star(data, stops[i], stops[i + 1], time_on_stop, opt_time)
        if last_line != None:
            if a_star_solution[0][0] != last_line:
                time_on_stop += 120
                a_star_solution = a_star(
                    data, stops[i], stops[i + 1], time_on_stop, opt_time
                )

        time_on_stop = a_star_solution[-1][-1]
        last_line = a_star_solution[-1][0]

    return time_on_stop


def calculate_solution(
    stops: list[str], time_on_stop: int, data: Dict[str, Stop], opt_time: bool = True
) -> list[Tuple[str, str, int]]:
    last_line = None
    solution = []
    for i in range(len(stops) - 1):
        a_star_solution = a_star(data, stops[i], stops[i + 1], time_on_stop, opt_time)
        if last_line != None:
            if a_star_solution[0][0] != last_line:
                time_on_stop += 120
                a_star_solution = a_star(
                    data, stops[i], stops[i + 1], time_on_stop, opt_time
                )

        solution.append(a_star_solution)
        time_on_stop = a_star_solution[-1][-1]
        last_line = a_star_solution[-1][0]

    return solution


def create_neighbourhood(route: list[str]) -> list[Tuple[str, str]]:
    solution = []

    path = route[1:-1]
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            solution.append((i + 1, j + 1))

    return solution


def sampling(stops: list[str], amount: int) -> list[str]:
    return random.sample(stops, amount)


def generate_diverse_neighbourhood(route: list[str]) -> list[Tuple[int, int, str]]:

    neighbours = []
    num_stops = len(route) - 2

    for _ in range(10):
        i, j = random.sample(range(1, num_stops + 1), 2)
        if (i, j) not in neighbours or (j, i) not in neighbours:
            neighbours.append((i, j))

    return neighbours


def tabu(
    start_stop: str,
    stops: list[str],
    time_on_stop: int,
    data: Dict[str, Stop],
    opt: str = "t",
) -> None:
    if opt == "t":
        opt_time = True
    else:
        opt_time = False

    iterations: int = 100
    no_improvement: int = 20

    timer = time.time()
    best_solution: list[str] = [start_stop] + stops + [start_stop]
    best_cost: int = calculate_cost(best_solution, time_on_stop, data, opt_time)
    tabu_list = set()

    num_stops = len(stops)
    tabu_list_size = int(math.sqrt(num_stops))
    tabu_queue = Queue(max(1, tabu_list_size))

    current_solution = best_solution
    neighbourhood = create_neighbourhood(current_solution)

    no_improvement_counter = 0

    while iterations > 0 and no_improvement > no_improvement_counter:
        iterations -= 1

        random.shuffle(neighbourhood)
        sampled_neighbours = neighbourhood[: math.ceil(num_stops / 2)]
        # new_neighbourhood = generate_diverse_neighbourhood(neighbourhood)
        # sampled_neighbours = random.sample(new_neighbourhood,max(len(new_neighbourhood),2))

        best_neighbour = None
        best_neighbour_cost = infinity

        for neighbour_indices in sampled_neighbours:
            i, j = neighbour_indices
            neighbour_solution = current_solution.copy()
            neighbour_solution[i], neighbour_solution[j] = (
                neighbour_solution[j],
                neighbour_solution[i],
            )
            neighbour_cost = calculate_cost(
                neighbour_solution, time_on_stop, data, opt_time
            )

            is_tabu = tuple(sorted(neighbour_indices)) in tabu_list

            if neighbour_cost < best_neighbour_cost:
                if not is_tabu or neighbour_cost < best_cost:
                    best_neighbour_cost = neighbour_cost
                    best_neighbour = neighbour_solution

        if best_neighbour:
            if best_neighbour_cost < best_cost:
                best_solution = best_neighbour
                best_cost = best_neighbour_cost
                no_improvement_counter = 0
            else:
                no_improvement_counter += 1

            tabu_list.add(tuple(sorted(neighbour_indices)))
            if tabu_queue.full():
                removed_move = tabu_queue.get()
                tabu_list.discard(removed_move)
            tabu_queue.put(tuple(sorted(neighbour_indices)))
            current_solution = best_neighbour

    solution = calculate_solution(best_solution, time_on_stop, data, opt_time)
    last_route = None

    sys.stderr.write(f"Total time: {time.time() - timer}\n")

    solution2 = []
    for i in range(len(solution)):
        if len(solution[i]) == 2:
            solution2.append([solution[i][0]])
            solution2.append([solution[i][1]])
        else:
            solution2.append(solution[i])

    solution2 = [y for x in solution2 for y in x]
    while solution2:
        route = solution2.pop(0)
        if not last_route:
            last_route = route
            continue

        if last_route[0] != route[0]:
            sys.stdout.write(
                f"Line {last_route[0]} | Departure: {seconds_to_time(last_route[2])} | Departure stop: {last_route[1]} | Arrival: {seconds_to_time(last_route[4])} | Arrival stop: {last_route[3]}\n"
            )
            last_route = route
        else:
            last_route = (
                last_route[0],
                last_route[1],
                last_route[2],
                route[3],
                route[4],
            )

    sys.stdout.write(
        f"Line {last_route[0]} | Departure: {seconds_to_time(last_route[2])} | Departure stop: {last_route[1]} | Arrival: {seconds_to_time(last_route[4])} | Arrival stop: {last_route[3]}\n"
    )


if __name__ == "__main__":
    data = load_data("./connection_graph.csv")
    data = remove_duplicates(data)
    stops: Dict[str, Stop] = process_data(data)

    tabu(
        "PL. GRUNWALDZKI",
        [
            "Katedra",
            "GALERIA DOMINIKAŃSKA",
            "Tramwajowa",
            "Chińska",
            "Komuny Paryskiej",
        ],
        time_to_seconds("12:00:00"),
        stops,
        opt="t",
    )
