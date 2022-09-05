'''
Uses the iCUE SDK to control the iCUE LEDs based on average screen color
'''

import fractions
import sys
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


def update_all_leds(all_leds, colors):
    '''
    Helper function which actually executes the SDK command
    '''

    cnt = len(all_leds)

    for idx in range(cnt):
        device_leds = all_leds[idx]
        for led in device_leds:
            led.r = int(colors[0])
            led.g = int(colors[1])
            led.b = int(colors[2])

        SDK.set_led_colors_buffer_by_device_index(idx, device_leds)

    SDK.set_led_colors_flush_buffer()

    time.sleep(1/24) # Update once per frame


def average_rgb(array_one, array_two):
    '''
    Helper function to average two RGB arrays
    '''
    return (np.array(array_one) + np.array(array_two)) / 2.0


def update_colors(all_leds, previous_colors, fraction):
    '''
    Gets the screen colors and executes the update against the SDK
    '''
    colors = get_color(fraction)

    if np.array_equal(colors, previous_colors):
        return previous_colors

    transition = average_rgb(previous_colors, colors)

    update_all_leds(all_leds, average_rgb(previous_colors, transition))
    update_all_leds(all_leds, average_rgb(transition, colors))
    update_all_leds(all_leds, colors)

    return colors


def get_color(fraction):
    '''
    Gets the average color on the main screen
    '''
    img = ImageGrab.grab()

    im_arr = np.frombuffer(img.tobytes(), dtype=np.uint8)
    im_arr = im_arr.reshape((img.size[1], img.size[0], 3))

    y_size = len(im_arr)
    y_area = int(y_size * fraction)
    im_arr = im_arr[y_size-y_area:y_size]

    avg_color_per_row = np.average(im_arr, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    # If under specific threshold, set to bright white
    # all_under_threshold = np.all(avg_color < 50)

    # if all_under_threshold:
    #     return [255, 255, 255]

    return avg_color


def main():
    '''
    Main Function Loop
    '''
    global SDK

    SDK = CueSdk()

    previous_colors = [0, 0, 0]

    connected = SDK.connect()
    if not connected:
        err = SDK.get_last_error()
        print(f'Handshake failed: {err}')
        return

    all_leds = get_available_leds()

    if not all_leds:
        return

    fraction = 0.20
    if len(sys.argv) > 1:
        fraction = int(sys.argv[1])/100

    SDK.request_control()

    while True:
        previous_colors  = update_colors(all_leds, previous_colors, fraction)

if __name__ == "__main__":
    main()
