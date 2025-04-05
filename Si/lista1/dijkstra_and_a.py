from stop import time_to_seconds, load_data, process_data, Dict, Stop
from load_data import remove_duplicates
from sys import maxsize as infinity
from utils import seconds_to_time, format_data
import geopy.distance
import time
import heapq
import time
from typing import Dict
import sys
from improvement import min_time_cost_binary_search, heuristic_improved
import math

PENALTY = 600


def min_time_cost(start: Stop, stop: Stop, time: int, cur_line: str | None):
    routes = start.routes.get(stop.name, [])
    min_time = infinity
    possible_route = None
    for route in routes:
        transfer = 0
        if cur_line:
            if cur_line != route.line:
                transfer = 120
        if route.start_time >= time + transfer:
            if route.end_time < min_time:
                min_time = route.end_time
                possible_route = route

    return possible_route


def min_transfer_cost(start: Stop, stop: Stop, time: int, cur_line: str | None):
    routes = start.routes.get(stop.name, [])
    min_time = infinity
    possible_route = None
    for route in routes:
        transfer = 0
        if cur_line:
            if cur_line != route.line:
                transfer = PENALTY
        if route.start_time >= time + transfer:
            if route.end_time < min_time:
                min_time = route.end_time
                possible_route = route

    return possible_route


def dijkstra_algorithm(
    data: Dict[str, Stop], stop_a: str, stop_b: str, time_on_stop: str
):

    time_on_stop = time_to_seconds(time_on_stop)
    timer = time.time()

    stops: Dict[str, Stop] = data

    q = stops.copy()
    stops_distances = {stop: infinity for stop in stops}
    stops_distances[stop_a] = time_on_stop
    previous_stop = {}
    previous_stop[stop_a] = (None, None, None, None)

    while q:
        v = min(q, key=lambda x: stops_distances[x])
        q.pop(v)

        if v == stop_b:
            break

        for next_stop in stops[v].routes:

            prev_line = previous_stop[v][1]
            route = min_time_cost_binary_search(
                stops[v], stops[next_stop], stops_distances[v], prev_line
            )
            if route:
                if route.end_time < stops_distances[next_stop]:

                    stops_distances[next_stop] = route.end_time
                    previous_stop[next_stop] = (
                        v,
                        route.line,
                        route.start_time,
                        route.end_time,
                        stops_distances[v],
                    )

    sys.stderr.write(f"Algorithm time: {time.time()-timer}\n")
    path = []

    current_stop = stop_b

    while current_stop != stop_a:

        prev, line, departure, arrival, end_time = previous_stop[current_stop]

        previous_stop.pop(current_stop)

        if departure is None or arrival is None:
            break

        path.append(
            (line, current_stop, seconds_to_time(arrival), seconds_to_time(departure))
        )
        current_stop = prev

    path.append((line, prev, seconds_to_time(departure), 0))

    formatted = format_data(path)
    for i in formatted:
        sys.stdout.write(i)


def a_star(
    data: Dict[str, Stop], stop_a: str, stop_b: str, time_on_stop: str, opt: str = "t"
):

    if opt == "t":
        opt_time = True
    else:
        opt_time = False

    time_on_stop = time_to_seconds(time_on_stop)
    stops = data
    timer = time.time()

    open_list = []
    heapq.heappush(
        open_list, (heuristic_improved(stops[stop_a], stops[stop_b]), stop_a)
    )

    closed_list = {}
    g = {stop_a: time_on_stop}
    f = {stop_a: heuristic_improved(stops[stop_a], stops[stop_b])}
    h = {stop_a: heuristic_improved(stops[stop_a], stops[stop_b])}
    previous_stop = {}
    previous_stop[stop_a] = (None, None, None, None)

    while open_list:
        _, current_stop = heapq.heappop(open_list)

        if current_stop == stop_b:
            break

        closed_list[current_stop] = True

        for next_stop in stops[current_stop].routes:
            if next_stop in closed_list:
                continue

            prev_line = previous_stop[current_stop][1]

            if opt_time:
                # possible_route = min_time_cost(
                #     stops[current_stop], stops[next_stop], g[current_stop], prev_line
                # )

                possible_route = min_time_cost_binary_search(
                    stops[current_stop], stops[next_stop], g[current_stop], prev_line
                )
            else:
                possible_route = min_transfer_cost(
                    stops[current_stop], stops[next_stop], g[current_stop], prev_line
                )

            if possible_route is None:
                continue

            tentative_g = possible_route.end_time

            if next_stop in g and tentative_g >= g[next_stop]:
                continue

            g[next_stop] = tentative_g
            h[next_stop] = h.get(
                next_stop, heuristic_improved(stops[next_stop], stops[stop_b])
            )
            f[next_stop] = h[next_stop] + g[next_stop]
            previous_stop[next_stop] = (
                current_stop,
                possible_route.line,
                possible_route.start_time,
                possible_route.end_time,
                g[current_stop],
            )

            heapq.heappush(open_list, (f[next_stop], next_stop))

    sys.stderr.write(f"\nCzas wykonania algorytmu: {time.time() - timer}\n")

    solution = []
    current_stop = stop_b

    while current_stop != stop_a:
        prev, line, departure, arrival, t = previous_stop[current_stop]
        previous_stop.pop(current_stop)
        if departure is None or arrival is None:
            break

        if len(solution) == 0:
            solution.append(
                (
                    line,
                    prev,
                    departure,
                    current_stop,
                    arrival,
                )
            )

        elif solution[-1][0] == line:
            solution[-1] = (
                line,
                prev,
                departure,
                solution[-1][3],
                solution[-1][4],
            )
        else:
            solution.append(
                (
                    line,
                    prev,
                    departure,
                    current_stop,
                    arrival,
                )
            )

        current_stop = prev

    solution.reverse()
    last_route = None
    while solution:

        route = solution.pop(0)
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


def heuristic(stop_a: Stop, stop_b: Stop):
    return geopy.distance.distance(
        (stop_a.lat, stop_a.lon), (stop_b.lat, stop_b.lon)
    ).km / (3 * 30)


if __name__ == "__main__":

    data = load_data("./connection_graph.csv")
    data = remove_duplicates(data)
    stops: Dict[str, Stop] = process_data(data)
    dijkstra_algorithm(
        data=stops, stop_a="BISKUPIN", stop_b="DWORZEC GŁÓWNY", time_on_stop="10:59:00"
    )
    a_star(
        data=stops,
        stop_a="BISKUPIN",
        stop_b="DWORZEC GŁÓWNY",
        time_on_stop="10:59:00",
        opt="t",
    )
    a_star(
        data=stops,
        stop_a="BISKUPIN",
        stop_b="DWORZEC GŁÓWNY",
        time_on_stop="10:59:00",
        opt="p",
    )
