from util_drive import Robot
import time
from util_neopix_buzzer import * 
from machine import Pin
import math
from util_ultrasound import Ultrasound
import neopixel
import asyncio


#Use neopixel and buzzer
buzzer = machine.PWM(machine.Pin(22))
# create the variable to handle distance sensing
ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
pixels = neopixel.NeoPixel(machine.Pin(18), 2)
duty_cycle = 0.9  # percentage
robot = Robot()



async def play_melody_async(melody, pixels, buzzer, duty_cycle=0.01):
    last_freq = None
    for note_name, duration in melodies[melody]:
        if note_name == "rest":
            if last_freq is not None:
                buzzer.freq(last_freq)
                buzzer.duty_u16(50)
            else:
                buzzer.duty_u16(0)
            pixels.fill((0, 0, 0))
            pixels.write()
            await asyncio.sleep(duration)
            continue

        note = get_note(note_name)
        if note:
            freq = int(note["frequency"])
            color = note["rgb"]
            last_freq = freq
            pixels.fill(color)
            pixels.write()
            buzzer.freq(freq)
            buzzer.duty_u16(int(65535 * duty_cycle))
            await asyncio.sleep(duration)
            buzzer.duty_u16(200)
            pixels.fill((0, 0, 0))
            pixels.write()
            await asyncio.sleep(0.02)
        else:
            buzzer.duty_u16(200)
            pixels.fill((0, 0, 0))
            pixels.write()
            await asyncio.sleep(duration)
# ---- ASYNC SONG TASK ----
async def play_song_task():
    await play_melody_async("sandstorm", pixels, buzzer, duty_cycle)
    


# ---- DANCING ROUTINE (ASYNC) ----
async def move(v, w, t_ms):
    robot.drive(v, w)
    await asyncio.sleep_ms(t_ms)
    robot.drive(0, 0)
    await asyncio.sleep_ms(120)


async def dance_task():
    # --- INTRO: four quick forward/back pulses ---
    for _ in range(4):
        await move(20, 0, 250)
        await move(-20, 0, 250)

    # --- SPIN BURST ---
    await move(0, math.radians(720), 900)

    # --- SMALL ARC SLICES ---
    for _ in range(3):
        await move(15, math.radians(180), 350)
        await move(15, -math.radians(180), 350)

    # --- SHIMMY SPIN POPS ---
    for _ in range(5):
        await move(0, math.radians(540), 200)

    # --- MICRO GLIDE ---
    await move(20, 0, 400)
    await move(-20, 0, 400)

    # --- TIGHT FIGURE-8 ---
    await move(10, math.radians(270), 600)
    await move(10, -math.radians(270), 600)

    # --- DOUBLE SPIN ---
    await move(0, -math.radians(720), 700)
    await move(0, math.radians(720), 700)

    # --- FINAL HEADSPINS ---
    for _ in range(3):
        await move(0, math.radians(1080), 250)

    # --- SIDE-STEP ROCK (~4.0 s) ---
    # Small arcs left/right so it "rocks" but stays near center.
    for _ in range(4):
        await move(10, math.radians(90), 400)
        await move(10, -math.radians(90), 400)

    # --- ORBIT GROOVE (~4.0 s) ---
    # Slow circle roughly in place; low v keeps radius small.
    for _ in range(4):
        await move(8, math.radians(180), 500)

    # --- RAPID SPIN BREAK (~3.0 s) ---
    for _ in range(6):
        await move(0, math.radians(720), 250)


    # End pose (same style as before, a bit longer) (~1.2 s)
    await move(10, 0, 400)
    await move(0, -math.radians(90), 400)
    robot.drive(0, 0)


# ---- MAIN ----
async def main():
    # Run both tasks at the same time
    await asyncio.gather(
        play_song_task(),
        dance_task()
    )


asyncio.run(main())










