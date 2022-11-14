from pynput.mouse import Button, Controller
import csv
import keyboard
import os

mouse = Controller()
_pth = os.getcwd()
_pth = os.path.join(_pth, "mouse.csv")

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (500, 500)
print('Now we have moved it to {0}'.format(
    mouse.position))

# Move pointer relative to current position

csv_file = open(_pth, "w")
csv = csv.writer(csv_file)
csv.writerow(["x", "y"])

while 1:
    p1 = mouse.position  # Becomes (100, 150)
    mouse.move(10, 20)
    p2 = mouse.position  # Becomes (110, 170)
    diff = (p2[0] - p1[0], p2[1] - p1[1])
    print("difference", diff)
    csv.writerow([diff[0], diff[1]])
    
    if keyboard.is_pressed("s"):
        csv_file.close()
        break
