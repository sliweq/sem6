from enum import Enum
from typing import Dict

from load_data import load_data
from utils import time_to_seconds


class Route_type(Enum):
    BUS = 1
    TRAM = 2


class Route:
    pass


class Stop:
    def __init__(self, name: str, lat: float, lon: float):
        self.name: str = name

        self.routes: Dict[str : list[Route]] = {}
        self.lat: float = lat
        self.lon: float = lon

    def add_stop(self, route: Route):
        if route.end_stop.name not in self.routes:
            self.routes[route.end_stop.name] = []

        self.routes[route.end_stop.name].append(route)


class Route:
    def __init__(
        self,
        route_type: Route_type,
        start_stop: Stop,
        end_stop: Stop,
        start_time: int,
        end_time: int,
        company: str,
        line: str,
    ):
        self.route_type: Route_type = route_type
        self.start_stop: Stop = start_stop
        self.end_stop: Stop = end_stop
        self.start_time: int = start_time
        self.end_time: int = end_time
        self.comapny: str = company
        self.travel_time: int = self.end_time - self.start_time
        self.line = line

    def __lt__(self, other):
        return self.start_time < other.start_time


def process_data(data: list[list[str]]) -> dict[str, Stop]:
    stops: Dict[str:Stop] = {}

    for row in data[1:]:
        # row schema: row_number, company (MPK TRAMWAJE - trams, rest buses), line number,
        # start_time (depart time), end time (arriv. time),
        #  start stop, end stop, start lat, start lon, end lat, end lon

        if row[5] not in stops.keys():
            stops[row[5]] = Stop(name=row[5], lat=row[7], lon=row[8])
        if row[6] not in stops.keys():
            stops[row[6]] = Stop(name=row[6], lat=row[9], lon=row[10])

        stops[row[5]].add_stop(
            Route(
                route_type=(
                    Route_type.TRAM if row[1] == "MPK Tramwaje" else Route_type.BUS
                ),
                start_stop=stops[row[5]],
                end_stop=stops[row[6]],
                start_time=time_to_seconds(row[3]),
                end_time=time_to_seconds(row[4]),
                company=row[1],
                line=row[2],
            )
        )

    for stop in stops.values():
        for routes in stop.routes.values():
            routes.sort()

    return stops


from load_data import load_data
from utils import time_to_seconds


def print_stop_info(stop_name: str, stops: Dict[str, Stop]):
    if stop_name in stops:
        stop = stops[stop_name]
        print(f"Przystanek: {stop.name}")
        print(f"Trasy przechodzące przez ten przystanek:")

        for start_stop, routes in stop.routes.items():
            for route in routes:
                print(
                    f"Linia {route.line} ({'Tramwaj' if route.route_type == Route_type.TRAM else 'Autobus'}), "
                    f"Od {route.start_time} do {route.end_time}, "
                    f"Przystanek początkowy: {route.start_stop.name}, "
                    f"Przystanek końcowy: {route.end_stop.name}"
                )
    else:
        print(f"Nie znaleziono przystanku o nazwie {stop_name}")


if __name__ == "__main__":
    data = load_data("./test_graph.csv")

    stops = process_data(data)

    print_stop_info("BISKUPIN", stops)
