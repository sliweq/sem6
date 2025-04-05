from stop import Dict, Stop
from sys import maxsize as infinity
import geopy.distance
import heapq
from typing import Dict
from improvement import heuristic_improved, min_time_cost_binary_search


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
                transfer = 600
        if route.start_time >= time + transfer:
            if route.end_time < min_time:
                min_time = route.end_time
                possible_route = route

    return possible_route


def a_star(
    data: Dict[str, Stop], stop_a: str, stop_b: str, time_on_stop: int, opt_time=True
):
    stops = data

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

    path = []
    current_stop = stop_b

    while current_stop != stop_a:
        prev, line, departure, arrival, t = previous_stop[current_stop]
        previous_stop.pop(current_stop)
        if departure is None or arrival is None:
            break

        if len(path) == 0:
            path.append(
                (
                    line,
                    prev,
                    departure,
                    current_stop,
                    arrival,
                )
            )

        elif path[-1][0] == line:
            path[-1] = (
                line,
                prev,
                departure,
                path[-1][3],
                path[-1][4],
            )
        else:
            path.append(
                (
                    line,
                    prev,
                    departure,
                    current_stop,
                    arrival,
                )
            )

        current_stop = prev

    path.reverse()
    return path


def heuristic(stop_a: Stop, stop_b: Stop):
    return geopy.distance.distance(
        (stop_a.lat, stop_a.lon), (stop_b.lat, stop_b.lon)
    ).km / (3 * 30)
