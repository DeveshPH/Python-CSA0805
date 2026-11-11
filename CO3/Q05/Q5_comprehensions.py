readings = [3.2, 7.1, 51.0, -55.0, 4.5, 1.2, 8.4]
valid = [x for x in readings if -50 <= x <= 50]
fahrenheit = [round(x * 9/5 + 32, 2) for x in valid]
alarms = [(minute, temp) for minute, temp in enumerate(readings)
          if not 2 <= temp <= 8]
print("valid C:", valid)
print("valid F:", fahrenheit)
print("alarm minutes:", alarms)
