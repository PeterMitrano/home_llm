import lifxlan

from gpt4all import GPT4All

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
You will be asked questions, and you should respond only python code, with all import statements needed.
Do not include any comments in the code or your response.
The return value of the code should be a dictionary.
"""


API_DOCS = """
API Documentation:

# color is a list of HSBK values: [hue (0-65535), saturation (0-65535), brightness (0-65535), Kelvin (2500-9000)]
# duration is the transition time in milliseconds
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
You can get Light objects automatically though LAN-based discovery (takes a few seconds), or by creating Light objects using a known MAC address and IP address:

lights = lan.get_lights()                              # Option 1: Discovery
light = Light("12:34:56:78:9a:bc", "192.168.1.42")     # Option 2: Direct
The Light API provides everything in the Device API, as well as:

# duration is the transition time in milliseconds
# is_transient is 1/0. If 1, return to the original color after the specified number of cycles. If 0, set light to specified color
# period is the length of one cycle in milliseconds

set_power(power, [duration])
set_color(color, [duration])
get_power()
get_color()
The Light API also provides macros for basic colors, like RED, BLUE, GREEN, etc. Setting colors is as easy as mybulb.set_color(BLUE). See light.py for complete list of color macros.

Finally, you can set parts of the color individually using the following four methods. However, the bulbs must receive all four values in each SetColor message. That means that using one of the following methods is always slower than using set_color(color) above because it will have to call get_color() first to get the other three values.

set_hue(hue, [duration])
set_brightness(brightness, [duration])
set_saturation(saturation, [duration])
set_colortemp(kelvin, [duration])

Group API
A Group is a collection of devices. Under the covers, a Group is just a list of device objects (like Devices, Lights, MultiZoneLights) and a set of functions that send multi-threaded commands to the applicable devices in the group. The multi-threading allows changes to be made more or less simultaneously. At the very least, it is certainly faster than if you looped through each individual light one at a time. You can get a Group by group, location, or device names via the LifxLAN API. However, you can also instantiate a Group with any arbitrary list of device objects. Here are some ways to create groups:

# The following methods use discovery
lan = LifxLAN()
g = lan.get_devices_by_name(["Left Lamp", "Right Lamp"])
g = lan.get_devices_by_group("Living Room")
g = lan.get_devices_by_location("My Home")

# This method is fastest
right = Light("12:34:56:78:9a:bc", "192.168.0.2")
left = Light("cb:a9:87:65:43:21", "192.168.0.3")
g = Group([right, left])
Almost all of the Group API methods are commands. Commands will only be sent to the devices in the group that support that capability. If you want to get state information from the devices, you will need to access the list of devices and call their get methods directly.

add_device(device_object)
remove_device(device_object)
remove_device_by_name(device_name)
get_device_list()
set_power(power, [duration])
set_color(color, [duration])
set_hue(hue, [duration])
set_brightness(brightness, [duration])
set_saturation(saturation, [duration])
set_colortemp(kelvin, [duration])
"""

def main():
    code_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # TODO: is there a coding specific model?
    chat_model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

    code_prompt = SEPERATOR.join([API_DOCS, CODE_FIXED_PROMPT])

    # # Test the repeatability
    # TEST_PROMPT = "Select 10 random numbers, with replacement, in the range 1-100."
    # for i in range(10):
    #     print(f"{i}:")
    #     with model.chat_session():
    #         print(model.generate(TEST_PROMPT))

    # Test whether a new "with model.chat_session" correctly "remembers" or "forgets"
    # with model.chat_session():
    #     model.generate("remember the number 4. When I ask you for my number, tell me it is 4.")
    #     print(model.generate("Tell me my number."))
    #
    # with model.chat_session():
    #     print(model.generate("Tell me my number."))


if __name__ == '__main__':
    main()
