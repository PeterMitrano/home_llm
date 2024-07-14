SEPERATOR = "\n---\n"

FIXED_PROMPT = """
You are a home assistant device.
The user will ask you questions, and you will respond with a mix of python code and natural language.
Your response should be in dictionary form, with keys "code", "language", "continue".
The vale of "continue" should be True if there needs to be further communication with the user, such as asking a clarifying question.
Keep language response as short as possible. 
You are able to execute the code before responding to the user, and use the values you return in your language response. 
Use the return value of the code to come up with the language response which answers the users question. 
"""

CODE_FIXED_PROMPT = """
You are a home assistant device.
You will be asked questions, and you should respond with only python code, with all import statements needed.
Your respond will be directly exec'd.
If it throws an error you will receive the error message and fix it. In this case, again only respond with code.
Do not include any comments in the code or your response.
The return value of the code should be a dictionary.
"""

API_DOCS = """
lifxlan API Documentation:
lan = LifxLAN() # example
# color is a list of HSBK values: [hue (0-65535), saturation (0-65535), brightness (0-65535), Kelvin (2500-9000)]
# times are in milliseconds
# name is the string label for the light, such as "Right Lamp"
# names is a list of name strings, such as ["Left Lamp", "Right Lamp"]
# group is a string label for a group, such as "Living Room"
# location is the string label for a location, such as "My Home"
get_lights()
get_color_lights()
get_multizone_lights()
get_tilechain_lights()                                                                       
get_device_by_name(name)
get_devices_by_name(names)
get_devices_by_group(group)
get_devices_by_location(location)
set_power_all_lights(power, [duration])
set_color_all_lights(color, [duration])                                             
get_power_all_lights()
get_color_all_lights()
Device API
In keeping with the LIFX protocol, all lights are devices, and so support the following methods:
# label is a string, 32 char max
# power can be "on"/"off", True/False, 0/1, or 0/65535
# arguments in [square brackets] are optional
set_label(label)
set_power(power)
get_mac_addr()
get_ip_addr()
get_service()
get_port()
get_label()
get_power()
get_host_firmware_tuple()
get_host_firmware_build_timestamp()
get_host_firmware_version()
get_wifi_info_tuple()
get_wifi_signal_mw()
get_wifi_tx_bytes()
get_wifi_rx_bytes()
get_wifi_firmware_tuple()
get_wifi_firmware_build_timestamp()
get_wifi_firmware_version()
get_version_tuple()
get_location()
get_location_tuple()
get_location_label()
get_location_updated_at
get_group()
get_group_tuple()
get_group_label()
get_group_updated_at
get_vendor()
get_product()
get_version()
get_info_tuple()
get_time()
get_uptime()
get_downtime()
is_light()
supports_color()
supports_temperature()
supports_multizone()
Light API
lights = lan.get_lights()                              # Discovery
The Light API provides everything in the Device API, as well as:
# is_transient is 1/0. If 1, return to the original color after the specified number of cycles. If 0, set light to specified color
set_power(power, [duration])
set_color(color, [duration])
get_power()
get_color()
The Light API also provides macros for basic colors, like RED, BLUE, GREEN, etc.
You can set parts of the color individually using the following four methods.
However, the bulbs must receive all four values in each SetColor message.
That means that using one of the following methods is always slower than using set_color(color) above.
set_hue(hue, [duration])
set_brightness(brightness, [duration])
set_saturation(saturation, [duration])
set_colortemp(kelvin, [duration])
"""

import lifxlan
from lifxlan import LifxLAN, WorkflowException
from gpt4all import GPT4All
from lifxlan import Light, Device, Group, GetGroup


def lifx_str(device):
    indent = ""
    s = ""
    try:
        device.refresh()
        s += device.device_characteristics_str(indent)
        s += indent + device.device_product_str(indent)
    except WorkflowException:
        pass
    return s


def main():
    code_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # TODO: is there a coding specific model?
    chat_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

    # Get the current names, groups, locations,
    lifx = lifxlan.LifxLAN(num_lights=3)
    devices = lifx.get_devices()
    device_descriptions = "\n".join([lifx_str(d) for d in devices])

    code_system_prompt = SEPERATOR.join([API_DOCS,
                                         f'Current devices:\n{device_descriptions}',
                                         CODE_FIXED_PROMPT])

    with code_model.chat_session(system_prompt=code_system_prompt):
        code_prompt = "Turn on all the lights."
        for _ in range(3):
            try:
                print("\nCODE PROMPT:")
                print(code_prompt)
                code_response = code_model.generate(code_prompt)
                print("\nCODE RESPONSE:")
                print(code_response)
                exec(code_response)
            except Exception as e:
                code_prompt = f"Your code produced this error, please try again. You may choose to produce code that will help debug as well. \n{str(e)}"

    # Once we've successfully executed the code, fine-tune the model so we don't make the same mistake again
    lan = lifxlan.LifxLAN()
    lights = lan.get_lights()
    lan.get_devices_by_group("")
    for light in lights:
        if "Bedroom" in str(light):
            device = Device(str(light))
            device.set_power(True)


if __name__ == '__main__':
    main()
