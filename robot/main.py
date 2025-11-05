from line_sensor import LineReader
import time
from machine import Pin

if __name__ == "__main__":
    reader = LineReader(
        pins=[Pin(5-x) for x in range(6)],
        positions=[-20, -12, -4, 4, 12, 20]
    )

    while True:
        reader.update()
        print(f"Offset: {reader.offset: 4.2f}\n")
        time.sleep(0.1)
        reader.offset = 0