from tuya_connector import TuyaOpenAPI

# Tuya API Credentials
ACCESS_ID = "your-access-id"
ACCESS_SECRET = "your-access-key"
DEVICE_ID = "your-device-id"
ENDPOINT = "TUYA_ENDPOINT"

# Initialize TuyaOpenAPI
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
openapi.connect()

# Function to send commands to the device


def send_command(command_code, value):
    commands = {"commands": [{"code": command_code, "value": value}]}
    response = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", commands)
    return response

# Light control functions


def turn_on_light():
    return send_command("switch_led", True)


def turn_off_light():
    return send_command("switch_led", False)


def set_light_color(color_name):
    colors = {
        "red": (0, 100, 100),
        "green": (120, 100, 100),
        "blue": (240, 100, 100),
        "yellow": (60, 100, 100),
        "purple": (280, 100, 100),
        "white": (0, 0, 100)  # White = 0% saturation
    }

    if color_name not in colors:
        print(f"Color {color_name} is not supported")
        return {"error": "Color not supported"}

    h, s, v = colors[color_name]

    # Convert to 8-bit format and HEX
    h_hex = f"{int(h * 255 / 360):02x}"
    s_hex = f"{int(s * 255 / 100):02x}"
    v_hex = f"{int(v * 255 / 100):02x}"

    # Form the `colour_data` string
    hex_color = f"01{h_hex}{s_hex}{v_hex}"

    payload = {"commands": [{"code": "colour_data", "value": hex_color}]}

    try:
        response = openapi.post(f"/v1.0/devices/{DEVICE_ID}/commands", payload)
        print(f"Tuya Response: {response}")
        return response
    except Exception as e:
        print(f"Error sending request: {e}")
        return {"error": str(e)}
