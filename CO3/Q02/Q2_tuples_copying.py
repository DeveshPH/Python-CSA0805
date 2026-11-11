import copy
rows, cols = 3, 4
bad = [[0] * cols] * rows
bad[0][1] = 7
good = [[0 for _ in range(cols)] for _ in range(rows)]
good[0][1] = 7
print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print(stops[(13.0418, 80.2341)])
try:
    stops[[13.0418, 80.2341]] = "invalid key"
except TypeError as exc:
    print(type(exc).__name__, exc)
nested = [[1], [2]]
shallow = copy.copy(nested)
deep = copy.deepcopy(nested)
nested[0].append(9)
print("shallow sees nested mutation:", shallow)
print("deep is independent:", deep)
