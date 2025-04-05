def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# ('9', 'DWORZEC GŁÓWNY', '11:22:00', '11:20:00')
# ('120', 'Wzgórze Partyzantów', '11:18:00', '11:16:00')
# ('120', 'Komuny Paryskiej (szkoła)', '11:16:00', '11:15:00')
# ('120', 'Komuny Paryskiej', '11:15:00', '11:14:00')
# ('120', 'Świstackiego', '11:14:00', '11:13:00')
# ('120', 'Na Niskich Łąkach', '11:13:00', '11:12:00')
# ('120', 'Rakowiecka', '11:12:00', '11:10:00')
# ('143', 'Międzyrzecka', '11:08:00', '11:06:00')
# ('143', 'Biegasa', '11:06:00', '11:05:00')
# ('1', 'Chełmońskiego', '11:00:00', '10:59:00')
# ('1', 'Piramowicza (Kampus Biskupin)', '10:59:00', '10:58:00')
# ('1', 'Spółdzielcza', '10:58:00', '10:57:00')
# ('1', 'BISKUPIN', '10:57:00', 0)

# Line 1 | Departure: 10:57:00 | Departure stop: BISKUPIN | Arrival: 11:00:00 | Arrival stop: Chełmońskiego
# Line 143 | Departure: 11:05:00 | Departure stop: Chełmońskiego | Arrival: 11:08:00 | Arrival stop: Międzyrzecka
# Line 120 | Departure: 11:10:00 | Departure stop: Międzyrzecka | Arrival: 11:18:00 | Arrival stop: Wzgórze Partyzantów
# Line 9 | Departure: 11:20:00 | Departure stop: Wzgórze Partyzantów | Arrival: 11:22:00 | Arrival stop: DWORZEC GŁÓWNY


def format_data(data):
    data.reverse()
    output = []
    output.append(
        (
            data[0][0],
            data[0][1],
            data[0][2],
        )
    )

    last = data[0]
    for i in range(1, len(data)):
        if output[-1][0] != data[i][0]:
            output.append((last[0], last[1], last[2]))
            output.append((data[i][0], last[1], data[i][3]))
        last = data[i]

    output.append((last[0], last[1], last[2]))

    return [
        f"Line {a[0]} | Departure: {a[2]} | Departure stop: {a[1]} | Arrival: {b[2]} | Arrival stop: {b[1]}\n"
        for a, b in zip(output[::2], output[1::2])
    ]
