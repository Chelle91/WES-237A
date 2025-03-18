import time
import asyncio
import socket
import json
import threading
from pynq.overlays.base import BaseOverlay
from pynq.lib.pmod import Pmod_IO, Pmod_ADC

# Load the PYNQ base overlay
base = BaseOverlay("base.bit")

# -------------------------------------------------------------------
# PMOD Pin Mapping
# -------------------------------------------------------------------
BALL_SWITCH_PIN = 0         # Tilt sensor (ball switch) on PMOD B pin 0
LIGHT_SENSOR_PIN = 1        # Light sensor on PMOD B pin 1
BUZZER_PIN = 4              # Buzzer on PMOD B pin 4 (active buzzer)
RGB_RED_PIN = 5             # RGB LED red on PMOD B pin 5
RGB_GREEN_PIN = 6           # RGB LED green on PMOD B pin 6
RGB_BLUE_PIN = 7            # RGB LED blue on PMOD B pin 7
# Joystick is connected to PMODA via PMOD AD2

# -------------------------------------------------------------------
# Initialize hardware objects
# -------------------------------------------------------------------
ball_switch = Pmod_IO(base.PMODB, BALL_SWITCH_PIN, 'in')
light_sensor = Pmod_IO(base.PMODB, LIGHT_SENSOR_PIN, 'in')
buzzer = Pmod_IO(base.PMODB, BUZZER_PIN, 'out')
red_led = Pmod_IO(base.PMODB, RGB_RED_PIN, 'out')
green_led = Pmod_IO(base.PMODB, RGB_GREEN_PIN, 'out')
blue_led = Pmod_IO(base.PMODB, RGB_BLUE_PIN, 'out')
# Use the older ADC method for the joystick on PMODA
adc = Pmod_ADC(base.PMODA)
buttons_gpio = base.buttons  # Onboard buttons

# -------------------------------------------------------------------
# Networking Configuration
# -------------------------------------------------------------------
PLAYER_NAME = "Player1"
SERVER_IP = "192.168.0.100"
SERVER_PORT = 5005
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Global state variables
game_started = False   # Set True when the game starts
exit_game = False      # Set True to exit the client
last_detected_action = "Waiting"  # To track the previous overall action

# Thresholds for analog sensors (adjust as needed)
light_threshold = 0.5          # Light sensor: success if reading < 0.5 (dark)
joy_neutral = 1.9995           # Joystick neutral reading
joy_threshold = 0.2            # Joystick: event if deviation > 0.2

# Buzzer duration (seconds)
beep_duration = 1.0

# -------------------------------------------------------------------
# Helper functions for LED and buzzer feedback
# -------------------------------------------------------------------
def set_rgb(r, g, b):
    """Set the RGB LED color."""
    red_led.write(r)
    green_led.write(g)
    blue_led.write(b)

def turn_off_rgb():
    """Turn off the RGB LED."""
    set_rgb(0, 0, 0)

def play_buzzer(duration=beep_duration):
    """Activate the buzzer for a short beep."""
    buzzer.write(1)
    time.sleep(duration)
    buzzer.write(0)

async def process_game_action(action):
    """
    Provide visual and audible feedback:
      - "success": LED green
      - "waiting": LED blue
    (Failure conditions can be added later.)
    """
    if action == "success":
        set_rgb(0, 1, 0)  # Green for success
    elif action == "waiting":
        set_rgb(0, 0, 1)  # Blue for waiting
    else:
        turn_off_rgb()

# -------------------------------------------------------------------
# Sensor monitoring and JSON message sending with change detection
# -------------------------------------------------------------------
async def monitor_sensors():
    global game_started, exit_game, last_detected_action

    while not exit_game:
        if not game_started:
            message = {
                "players": { PLAYER_NAME: {"action": "None", "result": "waiting", "successes": 0} },
                "button": 0, "tilt": 0, "light": 10, "joystick": 10,
                "time_left": 60, "status": "Waiting for start"
            }
            client.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))
            await asyncio.sleep(0.5)
            continue

        # --- Onboard buttons ---
        btn_state = buttons_gpio.read()  
        # Based on your tester, when a button is pressed, btn_state is nonzero.
        button_value = 10 if btn_state != 0 else 0
        print("Button reading:", bin(btn_state) if btn_state else btn_state)

        # --- Tilt sensor (ball switch) ---
        # Expected: resting state 1, tilted 0.
        tilt_reading = ball_switch.read()
        tilt_value = 10 if tilt_reading == 0 else 0
        print("Tilt sensor reading:", tilt_reading)

        # --- Light sensor ---
        light_reading = light_sensor.read()  # Expected float (0 to 1)
        light_value = 2 if light_reading < light_threshold else 10
        print("Light sensor reading:", light_reading)

        # --- Joystick via ADC (X and Y separately) ---
        try:
            x_raw = adc.read(1, 0, 0)  # X-axis (V1)
            y_raw = adc.read(0, 1, 0)  # Y-axis (V2)
            x_reading = x_raw[0] if isinstance(x_raw, list) else x_raw
            y_reading = y_raw[0] if isinstance(y_raw, list) else y_raw
        except Exception as e:
            print("ADC error:", e)
            x_reading = joy_neutral
            y_reading = joy_neutral
        print("Joystick X reading:", x_reading, "Joystick Y reading:", y_reading)
        joystick_value = 10
        detected_joystick_action = None
        if x_reading < joy_neutral - joy_threshold:
            detected_joystick_action = "STICK IT (LEFT)"
            joystick_value = 2
        elif x_reading > joy_neutral + joy_threshold:
            detected_joystick_action = "STICK IT (RIGHT)"
            joystick_value = 2
        elif y_reading < joy_neutral - joy_threshold:
            detected_joystick_action = "STICK IT (DOWN)"
            joystick_value = 2
        elif y_reading > joy_neutral + joy_threshold:
            detected_joystick_action = "STICK IT (UP)"
            joystick_value = 2

        # --- Determine overall detected action (priority: button > tilt > light > joystick) ---
        if button_value == 10:
            detected_action = "PUSH IT (BUTTON)"
            overall_success = True
        elif tilt_value == 10:
            detected_action = "TILT IT"
            overall_success = True
        elif light_value == 2:
            detected_action = "LIGHT IT"
            overall_success = True
        elif detected_joystick_action is not None:
            detected_action = detected_joystick_action
            overall_success = True
        else:
            detected_action = "Waiting"
            overall_success = False

        # Check for state change: if the detected action has changed from the last cycle and it's a success, buzz.
        if overall_success and detected_action != last_detected_action:
            play_buzzer(beep_duration)
        last_detected_action = detected_action

        # Set LED based on overall success.
        if overall_success:
            await process_game_action("success")
        else:
            await process_game_action("waiting")

        # Build JSON message for the GUI:
        message = {
            "players": {
                PLAYER_NAME: {
                    "action": detected_action,
                    "result": "success" if overall_success else "waiting",
                    "successes": 1 if overall_success else 0
                }
            },
            "button": button_value,
            "tilt": tilt_value,
            "light": light_value,
            "joystick": joystick_value,
            "time_left": 60,
            "status": "Game in progress"
        }
        client.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))
        await asyncio.sleep(0.5)

# -------------------------------------------------------------------
# Simulated game events (local feedback only)
# -------------------------------------------------------------------
async def monitor_game_events():
    global exit_game
    while not exit_game:
        await process_game_action("waiting")
        await asyncio.sleep(2)

# -------------------------------------------------------------------
# Exit listener thread for graceful exit
# -------------------------------------------------------------------
def exit_listener():
    global exit_game
    while True:
        user_input = input("Enter 'q' to quit: ")
        if user_input.lower() == 'q':
            exit_game = True
            break

# -------------------------------------------------------------------
# Main async function
# -------------------------------------------------------------------
async def main():
    global game_started, exit_game
    print("Client is running. Waiting for game start...")
    input("Press Enter when the GUI Start button is pressed...")
    game_started = True
    print("Game started. Sending sensor updates...")
    threading.Thread(target=exit_listener, daemon=True).start()
    game_event_task = asyncio.create_task(monitor_game_events())
    sensor_task = asyncio.create_task(monitor_sensors())
    try:
        await asyncio.gather(game_event_task, sensor_task)
    except asyncio.CancelledError:
        pass
    print("Exiting client...")

asyncio.run(main())
