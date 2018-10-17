#!/usr/bin/python3
from picamera import PiCamera
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import os
from os.path import isfile, join
import time as t

def snap_photo(save_dir):    
    date_time = t.strftime('%Y_%m_%d-%H:%M:%S.jpg')
    save_file = join(save_dir, date_time)
    GPIO.output(flash_pin, GPIO.HIGH)
    t.sleep(0.5)
    camera.capture(save_file)
    t.sleep(0.5)
    GPIO.output(flash_pin, GPIO.LOW)

main_cycle_save_directory = "/home/pi/larvae_agitator_cam/pics/main_cycle"
if not os.path.exists(main_cycle_save_directory):
    os.makedirs(main_cycle_save_directory)

b4_shake_save_directory = "/home/pi/larvae_agitator_cam/pics/b4_shake"
if not os.path.exists(b4_shake_save_directory):
    os.makedirs(b4_shake_save_directory)

post_shake_save_directory = "/home/pi/larvae_agitator_cam/pics/post_shake"
if not os.path.exists(post_shake_save_directory):
    os.makedirs(post_shake_save_directory)

flash_pin = 26
b4_shake_pin = 13
post_shake_pin = 19
sec_btw_pics = 60*5 ## for main cycle

camera = PiCamera()
GPIO.cleanup()
GPIO.setup(flash_pin, GPIO.OUT)
GPIO.setup(b4_shake_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(post_shake_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_main_cycle_photo_t = t.time()
last_b4_shake_photo_t = t.time()
last_post_shake_photo_t = t.time()

main_cycle_photo = True
b4_shake_photo = False
post_shake_photo = False

running = True
start_t = t.time()
try:
    while running:
        curr_t = t.time()
        if (curr_t - last_main_cycle_photo_t) >= sec_btw_pics and (curr_t -last_main_cycle_photo_t) >= 1:
            main_cycle_photo = True

        if GPIO.input(b4_shake_pin) == GPIO.HIGH and (curr_t - last_b4_shake_photo_t) >= 1:
            b4_shake_photo = True

        if GPIO.input(post_shake_pin) == GPIO.HIGH and (curr_t - last_post_shake_photo_t) >= 1:
            post_shake_photo = True

        if main_cycle_photo:
            snap_photo(main_cycle_save_directory)
            last_main_cycle_photo_t = t.time()
            main_cycle_photo = False

        if b4_shake_photo:
            snap_photo(b4_shake_save_directory)
            last_b4_shake_photo_t = t.time()
            b4_shake_photo = False

        if post_shake_photo:
            snap_photo(post_shake_save_directory)
            last_post_shake_photo_t = t.time()
            post_shake_photo = False

except KeyboardInterrupt:
    GPIO.cleanup()
