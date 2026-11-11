timetable = {
    "Chennai Central": {
        "Bengaluru": [{"train": "12609", "departure": "06:10", "platform": 4}],
        "Coimbatore": [{"train": "12675", "departure": "07:15", "platform": 2}]
    },
    "Egmore": {
        "Madurai": [{"train": "12637", "departure": "20:10", "platform": 5}]
    }
}
for station, destinations in timetable.items():
    for destination, trains in destinations.items():
        for train in trains:
            print(station, destination, train["train"], train["departure"], train["platform"])
