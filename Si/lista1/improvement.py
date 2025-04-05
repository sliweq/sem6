from stop import Stop, Route
import math
from sys import maxsize as infinity


def heuristic_improved(stop_a: Stop, stop_b: Stop):
    lat1, lon1 = float(stop_a.lat), float(stop_a.lon)
    lat2, lon2 = float(stop_b.lat), float(stop_b.lon)
    R = 6371

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c / (3 * 30)


def min_time_cost_binary_search(
    start: Stop, stop: Stop, current_time: int, current_line: str | None
) -> Route | None:
    routes = start.routes.get(stop.name, [])
    if not routes:
        return None

    left, right = 0, len(routes) - 1
    best_route_index = -1

    while left <= right:
        mid = (left + right) // 2
        if routes[mid].start_time >= current_time:
            best_route_index = mid
            right = mid - 1
        else:
            left = mid + 1

    if best_route_index == -1:
        return None

    while (
        best_route_index > 0
        and routes[best_route_index - 1].start_time
        == routes[best_route_index].start_time
    ):
        best_route_index -= 1

    min_end_time = infinity
    possible_route = None

    for i in range(best_route_index, len(routes)):
        route = routes[i]
        transfer_penalty = 120 if current_line and current_line != route.line else 0

        if route.start_time >= current_time + transfer_penalty:
            if route.end_time < min_end_time:
                min_end_time = route.end_time
                possible_route = route

    return possible_route
