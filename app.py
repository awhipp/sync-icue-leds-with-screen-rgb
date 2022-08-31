'''
Uses the iCUE SDK to control the iCUE LEDs based on average screen color
'''

import time

import numpy as np
from PIL import ImageGrab

from cuesdk import CueSdk
from cuesdk.structs import CorsairLedColor


def get_available_leds():
    '''
    Gets all the available iCUE LEDs
    '''

    leds = list()
    device_count = SDK.get_device_count()

    for device_index in range(device_count):
        led_positions = SDK.get_led_positions_by_device_index(device_index)
        led_colors = list(
            [CorsairLedColor(led, 0, 0, 0) for led in led_positions.keys()])
        leds.append(led_colors)

    return leds


def update_colors(all_leds):
    '''
    Updates all the available iCUE LEDs with the average color on the main screen
    '''
    cnt = len(all_leds)

    colors = get_color()

    for idx in range(cnt):
        device_leds = all_leds[idx]
        for led in device_leds:
            led.r = colors[0]
            led.g = colors[1]
            led.b = colors[2]

        SDK.set_led_colors_buffer_by_device_index(idx, device_leds)

    SDK.set_led_colors_flush_buffer()


def get_color():
    '''
    Gets the average color on the main screen
    '''
    img = ImageGrab.grab()

    im_arr = np.frombuffer(img.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape((img.size[1], img.size[0], 3))

    avg_color_per_row = np.average(im_arr, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return [
        int(avg_color[0]),
        int(avg_color[1]),
        int(avg_color[2])
    ]


def main():
    '''
    Main Function Loop
    '''
    global SDK

    SDK = CueSdk()

    connected = SDK.connect()
    if not connected:
        err = SDK.get_last_error()
        print(f'Handshake failed: {err}')
        return

    all_leds = get_available_leds()
    if not all_leds:
        return

    while True:
        update_colors(all_leds)
        time.sleep(1/24) # Frames per second to sleep between calcualtions

if __name__ == "__main__":
    main()
