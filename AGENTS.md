# AGENTS.md — CircuitPython rules for Physical Computing (ESP32-S3 Seminar)

Read this before writing or changing any code in this folder. This folder is the CIRCUITPY drive of a microcontroller running CircuitPython 10.x. The student is a beginner.

## First, every time
Start every reply with the robot emoji 🤖 on its own line. That is how the student knows you read this file.

## This board
YD-ESP32-S3 N16R8 on the screw-terminal expansion board. `boot_out.txt` in this folder confirms it. Use only the ESP32-S3 pin names and pin map below.
The boards have the 5V IN-OUT jumper soldered, so the 5V pin carries USB power and can feed lights, the servo, the DAC, and the amp.

## Rules
- This is CircuitPython, not MicroPython or desktop Python. Never use `machine`, `utime`, `Pin`, `RPi.GPIO`, `pip`, threads, or `asyncio` unless the student asks for asyncio.
- `code.py` runs on the board the moment it is saved. There is no run button, terminal command, or debugger. Output appears in VS Code's Serial Monitor.
- Built in, nothing to install: `board`, `time`, `random`, `math`, `os`, `digitalio`, `analogio`, `pwmio`, `busio`, `neopixel`, `rainbowio`, `touchio`, `keypad`, `audiocore`, `audiomixer`, `audiomp3`. Everything else comes from `lib/`, installed with circup: `circup install -a` installs every library `code.py` imports; `circup install <name>` installs one. When you use a library that may not be in `lib/`, say so and give the command.
- Wi-Fi names, passwords, and API keys live in `settings.toml` (`CIRCUITPY_WIFI_SSID`, `CIRCUITPY_WIFI_PASSWORD`, `ADAFRUIT_AIO_USERNAME`, `ADAFRUIT_AIO_KEY`) and are read with `os.getenv()`. Never put them in `code.py`. The board only joins 2.4 GHz networks.

## How this class writes code (follow exactly)
- First line of every program: a comment with its file name, e.g. `# dice_roll.py`. Use the student's file name if given.
- Shape, in this order: imports → setup (hardware objects, constants) → functions → one `print()` → `while True:`. Define functions above `while True:` and call them inside it.
- Imports: built-in modules together on one line, e.g. `import board, neopixel, time`. Each library from `lib/` (`import adafruit_mpr121`) and each `from ... import ...` line goes on its own line below that. Colors: `from adafruit_led_animation.color import RED, GREEN, BLUE, ...` (also YELLOW, ORANGE, PURPLE, PINK, CYAN, TEAL, JADE, GOLD, AMBER, AQUA, MAGENTA, WHITE, BLACK), or `(R, G, B)` tuples 0–255.
- Just before `while True:`, print that the program is running and what to do: `print("dice_roll.py is running! Press button A to roll")`.
- Every `while True:` has a short `time.sleep()` unless it drives an animation or a debounced button that must be checked every pass.
- Names: `snake_case` for variables and functions (`distance_sensor`, `play_sound`), `ALL_CAPS` for constants (`NUM_PIXELS`, `SLEEP_TIME`), `UpperCamelCase` only for library classes. Descriptive names, never `x1` or `tmp`. Buttons are `button_A`, `button_B`.
- f-strings for printing: `print(f"Distance: {distance:.1f} cm")`. Write `if not button_A.value:` rather than `== False`.
- Rainbow colors: `colorwheel()` from the built-in `rainbowio` module. Never write your own `wheel()` function. To convert one range to another (a 0–65535 reading to 0–180 degrees), use `map_range` from `adafruit_simplemath`.
- Buttons and touch pads that should fire once per press use `adafruit_debouncer.Button` (`.update()` every loop, then `.pressed` / `.released`). Prefer it over `keypad`; it reads like English.
- No classes, `def main()`, `if __name__ == "__main__":`, decorators, type hints, blanket try/except, or threads. One job per function. A beginner must be able to read every line.
- 4-space indents, never tabs. Straight quotes only.
- When changing code: change only what was asked, keep the student's names, pins, and setup, show the COMPLETE `code.py`, then explain the change in two or three plain sentences.
- When the student pastes an assignment, keep its exact file name, variable names, colors, timings, and behavior rules.
- If the request is unclear (how many lights, which colors, how fast, which pin), ask one question before writing code.

## Power (check every program)
- Everything runs from one laptop USB port. NeoPixel brightness stays at 0.3 or lower (the strip has 100 lights).
- Warn, in a comment and one sentence, when a program exceeds those limits, lights more than about 30 pixels white, moves a servo while lights are on, or plays sound with many bright lights. Low power looks like flicker, a jittering servo, squealing audio, or a board that restarts ("Power dipped" safe mode → press RST, then reduce the load).
- Potentiometers and STEMMA-QT sensors run on 3.3V, never 5V. A separate 5V supply for lights or motors shares GND with the board but never touches the board's 5V pin.

## ESP32-S3 — YD-ESP32-S3 N16R8 on the screw-terminal expansion board
Pin names: `board.GPIO#` only (e.g. `board.GPIO15`). There is NO `board.IO15`, `board.D15`, `board.GP15`, `board.A0`, `board.I2C()`, or `board.STEMMA_I2C()`; build buses with `busio`. Extras: `board.NEOPIXEL` (one onboard status light), `board.BOOT` (button, `False` when pressed). Power pins: 5V, 3V3. No `audiopwmio` or `audioio` on this board; all sound goes through the I2S DAC. Wi-Fi is 2.4 GHz only.
| Device | Pins (wire color) | Setup |
|---|---|---|
| NeoPixel strip, 100 lights | GPIO15 (white), 5V (red), GND (black) | `neopixel.NeoPixel(board.GPIO15, 100, brightness=0.2)` |
| 32×8 NeoPixel matrix (256 lights) | same pins | `neopixel.NeoPixel(board.GPIO15, 256, brightness=0.1, auto_write=False)`; `PixelFramebuffer(pixels, 32, 8, orientation=VERTICAL, rotation=0)` from `adafruit_pixel_framebuf`; text needs `font5x8.bin` in the root of CIRCUITPY |
| Buttons (wired to GND, pressed == `False`) | GPIO6, GPIO7 | `switch_to_input(pull=digitalio.Pull.UP)` |
| Servo | GPIO13 (orange); 2nd servo GPIO12; red → 5V | `servo.Servo(pwmio.PWMOut(board.GPIO13, frequency=50), min_pulse=650, max_pulse=2350)` |
| Potentiometer | GPIO1 (white), red → 3V3 | `AnalogIn(board.GPIO1)`, then rescale with `MAX_READING` (see "Things that trip people up") |
| I2S DAC (PCM5102) + amp | WSEL GPIO16 (green), DIN GPIO17 (purple), BCK GPIO18 (gray); DAC Lout → amp (white); both VIN → 5V | `audio = audiobusio.I2SOut(bit_clock=board.GPIO18, word_select=board.GPIO16, data=board.GPIO17)` |
| STEMMA-QT sensors | blue SDA GPIO4, yellow SCL GPIO5, red → 3V3 | `i2c = busio.I2C(board.GPIO5, board.GPIO4)` (clock first, then data) |

## Things that trip people up
- Sound files live in `sounds/` (DJ loops in `funky/`). The folder name and `path = "sounds/"` must match exactly, including the slash. WAVs: 22050 Hz, 16-bit, mono. MP3s: mono, 22050 or 44100 Hz, constant bit rate 64–128 kbps, no album art. `while audio.playing: pass` freezes the lights until the sound ends; put light changes inside that loop if they must happen during a sound.
- MP3: create one `MP3Decoder("sounds/name.mp3")` at the top (it uses a lot of memory), then `decoder.open(path + filename)` to switch files and `audio.play(decoder)`. MP3s play one at a time. To layer sounds use WAVs with `audiomixer.Mixer(voice_count=..., sample_rate=22050, channel_count=1, bits_per_sample=16, samples_signed=True)`, `audio.play(mixer)` once, then `mixer.voice[i].play(wave, loop=True)` and `.level` 0.0–1.0.
- Potentiometer: on this board the analog reading never reaches 65535; it tops out near 62000. Every program that reads the pot rescales it exactly like this, so the rest of the code can assume 0–65535:
  ```python
  MAX_READING = 62000  # ESP32 reads max a bit low, so we recalibrate

  reading = potentiometer.value
  reading = int(reading / MAX_READING * 65535)
  reading = min(reading, 65535)  # This should give us a value between 0 and 65535
  ```
- VL53L1X distance sensor (`adafruit_vl53l1x`, I2C 0x29): call `distance_sensor.start_ranging()` once before the loop. `distance_sensor.distance` is centimeters and is `None` (not NaN, not 0) when nothing is in range, so check `if distance is None:` before any math. `distance_mode = 1` is short range and steadier indoors; 2 is long range.
- MPR121 touch sensor (`adafruit_mpr121`, I2C 0x5A): `touched_pins` is a tuple of 12 `True`/`False` values. React once per touch by comparing with the previous reading (example below) or wrap each pad in `Button(touch_sensor[i], value_when_pressed=True)`.
- `adafruit_debouncer.Button` does nothing unless `.update()` runs every loop.
- Servos: a noisy analog reading makes a servo wobble, so move it only when the new angle differs from the last by 2° or more, and sleep 0.05 s in the loop. `servo.angle = None` releases it.
- "No pull up found on SDA or SCL": the STEMMA-QT sensor isn't powered or SDA/SCL are swapped. "No I2C device at address": wrong sensor or loose cable.
- `ValueError: ... in use`: two objects on one pin; fix the code, then Ctrl-D. `ImportError: no module named`: `circup install -a`. `incompatible .mpy file`: `circup update --all`.

## Example program (follow this shape)
```python
# touch_pads.py
import board, busio, time
import adafruit_mpr121

i2c = busio.I2C(board.GPIO5, board.GPIO4)  # clock (yellow) GPIO5, data (blue) GPIO4
touch_sensor = adafruit_mpr121.MPR121(i2c)
previous_touches = (False,) * 12  # no pads touched yet

print("touch_pads.py is running! Touch and release pads 0-11")
while True:
    current_touches = touch_sensor.touched_pins  # 12 True/False values, one per pad
    for pad, is_touched in enumerate(current_touches):
        if is_touched and not previous_touches[pad]:
            print(f"Pad {pad} touched")
        elif previous_touches[pad] and not is_touched:
            print(f"Pad {pad} released")
    previous_touches = current_touches
    time.sleep(0.05)
```
