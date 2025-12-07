from util_ultrasound import Ultrasound
from machine import Pin
import time
import neopixel

global buzzer, pixels, duty_cycle, ultrasound

note_data = [
    # Octave 3
    {"note": "C3", "frequency": 130.81, "color_name": "Red", "rgb": (255, 0, 0), "distance_cm": 80},
    {"note": "C#3/Db3", "frequency": 138.59, "color_name": "Orange-Red", "rgb": (255, 69, 0), "distance_cm": 70},
    {"note": "D3", "frequency": 146.83, "color_name": "Orange", "rgb": (255, 140, 0), "distance_cm": 60},
    {"note": "D#3/Eb3", "frequency": 155.56, "color_name": "Yellow", "rgb": (255, 255, 0), "distance_cm": 50},
    {"note": "E3", "frequency": 164.81, "color_name": "Chartreuse", "rgb": (127, 255, 0), "distance_cm": 40},
    {"note": "F3", "frequency": 174.61, "color_name": "Green", "rgb": (0, 255, 0), "distance_cm": 30},
    {"note": "F#3/Gb3", "frequency": 185.00, "color_name": "Spring Green", "rgb": (0, 255, 127), "distance_cm": 25},
    {"note": "G3", "frequency": 196.00, "color_name": "Cyan", "rgb": (0, 255, 255), "distance_cm": 20},
    {"note": "G#3/Ab3", "frequency": 207.65, "color_name": "Azure", "rgb": (0, 127, 255), "distance_cm": 18},
    {"note": "A3", "frequency": 220.00, "color_name": "Blue", "rgb": (0, 0, 255), "distance_cm": 15},
    {"note": "A#3/Bb3", "frequency": 233.08, "color_name": "Violet", "rgb": (139, 0, 255), "distance_cm": 12},
    {"note": "B3", "frequency": 246.94, "color_name": "Magenta", "rgb": (255, 0, 255), "distance_cm": 10},

    # Octave 4 (original data)
    {"note": "C4", "frequency": 261.63, "color_name": "Red", "rgb": (255, 0, 0), "distance_cm": 40},
    {"note": "C#4/Db4", "frequency": 277.18, "color_name": "Orange-Red", "rgb": (255, 69, 0), "distance_cm": 35},
    {"note": "D4", "frequency": 293.66, "color_name": "Orange", "rgb": (255, 140, 0), "distance_cm": 30},
    {"note": "D#4/Eb4", "frequency": 311.13, "color_name": "Yellow", "rgb": (255, 255, 0), "distance_cm": 25},
    {"note": "E4", "frequency": 329.63, "color_name": "Chartreuse", "rgb": (127, 255, 0), "distance_cm": 20},
    {"note": "F4", "frequency": 349.23, "color_name": "Green", "rgb": (0, 255, 0), "distance_cm": 15},
    {"note": "F#4/Gb4", "frequency": 369.99, "color_name": "Spring Green", "rgb": (0, 255, 127), "distance_cm": 10},
    {"note": "G4", "frequency": 392.00, "color_name": "Cyan", "rgb": (0, 255, 255), "distance_cm": 8},
    {"note": "G#4/Ab4", "frequency": 415.30, "color_name": "Azure", "rgb": (0, 127, 255), "distance_cm": 6},
    {"note": "A4", "frequency": 440.00, "color_name": "Blue", "rgb": (0, 0, 255), "distance_cm": 5},
    {"note": "A#4/Bb4", "frequency": 466.16, "color_name": "Violet", "rgb": (139, 0, 255), "distance_cm": 4},
    {"note": "B4", "frequency": 493.88, "color_name": "Magenta", "rgb": (255, 0, 255), "distance_cm": 3},

    # Octave 5
    {"note": "C5", "frequency": 523.25, "color_name": "Red", "rgb": (255, 0, 0), "distance_cm": 20},
    {"note": "C#5/Db5", "frequency": 554.37, "color_name": "Orange-Red", "rgb": (255, 69, 0), "distance_cm": 18},
    {"note": "D5", "frequency": 587.33, "color_name": "Orange", "rgb": (255, 140, 0), "distance_cm": 16},
    {"note": "D#5/Eb5", "frequency": 622.25, "color_name": "Yellow", "rgb": (255, 255, 0), "distance_cm": 14},
    {"note": "E5", "frequency": 659.25, "color_name": "Chartreuse", "rgb": (127, 255, 0), "distance_cm": 12},
    {"note": "F5", "frequency": 698.46, "color_name": "Green", "rgb": (0, 255, 0), "distance_cm": 10},
    {"note": "F#5/Gb5", "frequency": 739.99, "color_name": "Spring Green", "rgb": (0, 255, 127), "distance_cm": 8},
    {"note": "G5", "frequency": 783.99, "color_name": "Cyan", "rgb": (0, 255, 255), "distance_cm": 6},
    {"note": "G#5/Ab5", "frequency": 830.61, "color_name": "Azure", "rgb": (0, 127, 255), "distance_cm": 5},
    {"note": "A5", "frequency": 880.00, "color_name": "Blue", "rgb": (0, 0, 255), "distance_cm": 4},
    {"note": "A#5/Bb5", "frequency": 932.33, "color_name": "Violet", "rgb": (139, 0, 255), "distance_cm": 3},
    {"note": "B5", "frequency": 987.77, "color_name": "Magenta", "rgb": (255, 0, 255), "distance_cm": 2},
    {"note": "rest", "frequency": 10.0, "color_name": "Magenta", "rgb": (255, 0, 255), "distance_cm": 2}
]

melodies = {
    "mario": [
        # Opening fanfare (iconic "Green Hill Zone" inspired)
        ("E4", 0.15), ("E4", 0.15), ("E4", 0.15),
        ("C4", 0.10), ("E4", 0.15), ("G4", 0.3),
        ("G3", 0.3), ("C4", 0.2), ("G3", 0.2), ("E3", 0.2),

        # Add a little syncopation and octave jumps
        ("A3", 0.15), ("B3", 0.15), ("A#3", 0.1), ("A3", 0.15),
        ("G3", 0.1), ("E4", 0.15), ("G4", 0.15), ("A4", 0.25),

        # Added flourish (ascending energy)
        ("C5", 0.2), ("B4", 0.15), ("A4", 0.15),
        ("G4", 0.15), ("E4", 0.15), ("C4", 0.15), ("A3", 0.25),

        # Playful bounce motif
        ("F4", 0.15), ("G4", 0.15), ("E4", 0.25), ("C4", 0.15),
        ("D4", 0.15), ("B3", 0.25),

        # New section (faster "looping" Sonic vibe)
        ("C4", 0.10), ("E4", 0.10), ("G4", 0.10), ("C5", 0.15),
        ("B4", 0.10), ("A4", 0.10), ("G4", 0.15),
        ("E4", 0.10), ("C4", 0.15), ("A3", 0.20), ("G3", 0.20),

        # Ending lift
        ("E4", 0.15), ("G4", 0.15), ("C5", 0.25), ("E5", 0.4),
        ("G4", 0.2), ("E4", 0.2), ("C4", 0.4)
    ],

    "pokemon": [
        # Verse 1 - "I wanna be the very best"
        ("E4", 0.25), ("F4", 0.25), ("G4", 0.5),
        ("E4", 0.25), ("F4", 0.25), ("G4", 0.5),
        ("A4", 0.25), ("A4", 0.25), ("A4", 0.5),
        ("G4", 0.25), ("F4", 0.25), ("E4", 0.5),

        # Verse 2 - "Like no one ever was"
        ("C4", 0.25), ("D4", 0.25), ("E4", 0.5),
        ("C4", 0.25), ("D4", 0.25), ("E4", 0.5),
        ("F4", 0.25), ("F4", 0.25), ("F4", 0.5),
        ("E4", 0.25), ("D4", 0.25), ("C4", 0.5),

        # Build-up with octave layering
        ("E4", 0.25), ("F4", 0.25), ("G4", 0.5),
        ("E4", 0.25), ("F4", 0.25), ("G4", 0.5),
        ("A4", 0.25), ("A4", 0.25), ("A4", 0.5),
        ("G4", 0.25), ("F4", 0.25), ("E4", 0.5),

        # Bridge - "To train them is my cause"
        ("C4", 0.25), ("D4", 0.25), ("E4", 0.5),
        ("C4", 0.25), ("D4", 0.25), ("E4", 0.5),
        ("F4", 0.25), ("G4", 0.25), ("A4", 0.75),
        ("G4", 0.25), ("A4", 0.25), ("C5", 0.5),

        # Chorus - "POKÉMON!"
        ("A4", 0.3), ("A4", 0.3), ("A4", 0.3),
        ("G4", 0.2), ("F4", 0.2), ("E4", 0.4),
        ("C5", 0.5), ("A4", 0.25), ("F4", 0.25), ("G4", 0.6),

        # Gotta catch 'em all - richer version with octave support
        ("A4", 0.25), ("B4", 0.25), ("C5", 0.5),
        ("C5", 0.25), ("B4", 0.25), ("A4", 0.5),
        ("F4", 0.25), ("G4", 0.25), ("A4", 0.6),
        ("E5", 0.4), ("C5", 0.25), ("A4", 0.25),

        # Tag ending - emotional resolve
        ("A4", 0.25), ("G4", 0.25), ("E4", 0.5),
        ("A4", 0.25), ("G4", 0.25), ("E4", 0.5),
        ("C4", 0.25), ("D4", 0.25), ("E4", 0.5),
        ("C5", 0.4), ("A4", 0.25), ("F4", 0.25), ("C4", 0.6)
    ],

    "sandstorm": [
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),
        ("rest", 0.08),
        ("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),
        ("rest", 0.08),
        ("A3", 0.08),("A3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),
        ("rest", 0.08),
        ("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),
        ("rest", 0.08),
        ("A3", 0.08),("A3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),
        ("rest", 0.08),
        ("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),
        ("rest", 0.08),
        ("A3", 0.08),("A3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),("E4", 0.08),
        ("rest", 0.08),
        ("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),("D4", 0.08),
        ("rest", 0.08),
        ("A3", 0.08),("A3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("E4", 0.08),("E4", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),("B3", 0.08),
        ("rest", 0.08),
        ("E4", 0.08),("E4", 0.08),("B3", 0.08),
        ("rest", 1.0),
    ],

    "victory_short": [
        ("C4", 0.20),
        ("E4", 0.20),
        ("G4", 0.25),

        ("C5", 0.20),
        ("E5", 0.20),
        ("C5", 0.30),

        ("G4", 0.20),
        ("C5", 0.45)
    ]
}

def get_note(note_name):
    for n in note_data:
        if n["note"].startswith(note_name):
            return n
    return None

def play_melody(melody, pixels, buzzer, duty_cycle=0.01):
    last_freq = None

    for note_name, duration in melodies[melody]:
        # Special handling for symbolic rest
        if note_name == "rest":
            # Optional: keep PWM at a tiny duty on the last frequency to avoid a pop
            if last_freq is not None:
                buzzer.freq(last_freq)
                buzzer.duty_u16(50)   # very small duty -> almost silent
            else:
                buzzer.duty_u16(0)

            # LEDs off during rest
            pixels.fill((0, 0, 0))
            pixels.write()

            time.sleep(duration)
            continue

        # Normal note path
        note = get_note(note_name)
        if note:
            freq = int(note["frequency"])
            color = note["rgb"]
            last_freq = freq

            # light up pixel
            pixels.fill(color)
            pixels.write()

            # play tone
            buzzer.freq(freq)
            buzzer.duty_u16(int(65535 * duty_cycle))
            time.sleep(duration)

            # short, softer pause between notes (tiny duty instead of full off)
            buzzer.duty_u16(200)   # experiment with 100–500
            pixels.fill((0, 0, 0))
            pixels.write()
            time.sleep(0.02)       # shorter gap also helps reduce clicking
        else:
            # Fallback rest if note_name not found
            buzzer.duty_u16(200)
            pixels.fill((0, 0, 0))
            pixels.write()
            time.sleep(duration)
    buzzer.duty_u16(0)
    buzzer.deinit()

def normal_mode(ultrasound, pixels, buzzer, duty_cycle):
    # measure the distance
    distance = ultrasound.measure()

    if distance is not None:
        # default values
        frequency = 0
        color = (0, 0, 0)
        for note in note_data:
            if note["distance_cm"] <= distance:
                color = note["rgb"]
                frequency = note["frequency"]
                break

        # Apply color to NeoPixel
        pixels.fill(color)
        pixels.write()
        # Play tone
        if frequency > 0:
            buzzer.freq(int(frequency))
            buzzer.duty_u16(int(65535 * duty_cycle))
        else:
            buzzer.duty_u16(0)
        time.sleep(0.1)
        
    else:
        frequency = 0
        color = (0, 0, 0)
    time.sleep(0.1)

if __name__ == "__main__":
    # create the buzzer
    buzzer = machine.PWM(machine.Pin(22))
    # create the variable to handle distance sensing
    ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))

    pixels = neopixel.NeoPixel(machine.Pin(18), 2)

    duty_cycle = 0.5  # percentage

    play_melody("victory_short", pixels, buzzer)
    
    
