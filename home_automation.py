import blynklib
import speak

BLYNK_AUTH_TOKEN = "your_blynk_auth_token"

blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN)

def control_device(device, action):
    device_pins = {
        "light": "V1",
        "fan": "V2",
        "tv": "V3"
    }

    pin = device_pins.get(device.lower())
    if not pin:
        speak.speak(f"I couldn't find the device {device}.")
        return

    if action.lower() in ["on", "off"]:
        state = 1 if action.lower() == "on" else 0
        blynk.virtual_write(pin, state)
        speak.speak(f"{device.capitalize()} turned {action}.")
    else:
        speak.speak(f"Invalid action {action} for {device}.")

#(keep active)
def run_blynk():
    while True:
        blynk.run()
