# ==============================================================================================
#
#      Github link:
#      https://github.com/Bluewave2/Drift-Script
#
#
#      Mouse = X axis steering
#      W = Throttle
#      S = Brake
#      C = Clutch
#      Q = Upshift (sequential)
#      E = Downshift (sequential)
#      R = Reset car (if the game supports it)
#      Z = View left
#      X = View right
#      Space = Handbrake
#      Mouse 3 = Lock mouse to bottom of screen (toggle)
#
# ==============================================================================================
if starting:    
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 5
    
    def set_button(button, key):
        if keyboard.getKeyDown(key):
            v.setButton(button, True)
        else:
            v.setButton(button, False)
    
    def calculate_rate(max, time):
        if time > 0:
            return max / (time / system.threadExecutionInterval)
        else:
            return max

    int32_max = (2 ** 14) - 1
    int32_min = (( 2** 14) * -1) + 1
    
    v = vJoy[0]
    v.x, v.y, v.z, v.rx, v.ry, v.rz, v.slider, v.dial = (int32_min,) * 8

    from ctypes import *

    user32 = windll.user32

    # =============================================================================================
    # Axis inversion settings (multiplier): normal = 1; inverted = -1
    # =============================================================================================
    global throttle_inversion, braking_inversion, clutch_inversion, hbrake_inversion
    throttle_inversion = 1
    braking_inversion = 1
    clutch_inversion = 1
    hbrake_inversion = 1
    
    # =============================================================================================
    # Mouse settings
    # =============================================================================================
    global mouse_sensitivity, sensitivity_center_reduction
    mouse_sensitivity = 5
    sensitivity_center_reduction = 1.0
    
    # =============================================================================================
    # Ignition cut settings
    # =============================================================================================
    global ignition_cut_time, ignition_cut_elapsed_time
    ignition_cut_enabled = True
    ignition_cut_time = 100
    ignition_cut_elapsed_time = 0
    
    global ignition_cut, ignition_cut_released
    # Init values, do not change
    ignition_cut = False
    ignition_cut_released = True
    
    # =============================================================================================
    # Steering settings
    # =============================================================================================
    global steering, steering_max, steering_min, steering_center_reduction    
    # Init values, do not change
    steering = 0.0
    steering_max = float(int32_max)
    steering_min = float(int32_min)
    steering_center_reduction = 1
    
    # =============================================================================================
    # Throttle settings
    # =============================================================================================
    global throttle_blip_enabled
    throttle_blip_enabled = False
    
    # In milliseconds
    throttle_increase_time = 100
    throttle_increase_time_after_ignition_cut = 0
    throttle_increase_time_blip = 50
    throttle_decrease_time = 150
    
    global throttle, throttle_max, throttle_min, throttle_max2
    # Init values, do not change
    throttle_max = int32_max * throttle_inversion
    throttle_min = int32_min * throttle_inversion
    throttle_max2 = int32_max * throttle_inversion
    throttle = throttle_min
    
    global throttle_increase_rate, throttle_decrease_rate
    # Set throttle behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    throttle_increase_rate = calculate_rate(throttle_max, throttle_increase_time)
    throttle_increase_rate_after_ignition_cut = calculate_rate(throttle_max, throttle_increase_time_after_ignition_cut) 
    throttle_increase_rate_blip = calculate_rate(throttle_max, throttle_increase_time_blip)
    throttle_decrease_rate = calculate_rate(throttle_max, throttle_decrease_time) * -1
    
    # =============================================================================================
    # Braking settings
    # =============================================================================================
    # In milliseconds
    braking_increase_time = 120
    braking_decrease_time = 120
    
    global braking, braking_max, braking_min, braking_max2, brakeflippy
    # Init values, do not change
    braking_max = int32_max * braking_inversion
    braking_min = int32_min * braking_inversion
    braking_max2 = braking_max
    brakeflippy = 0
    braking = braking_min
    
    global braking_increase_rate, braking_decrease_rate
    # Set braking behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    braking_increase_rate = calculate_rate(braking_max, braking_increase_time)
    braking_decrease_rate = calculate_rate(braking_max, braking_decrease_time) * -1
    
    # =============================================================================================
    # HBraking settings
    # =============================================================================================
    # In milliseconds
    hbrake_increase_time = 100
    hbrake_decrease_time = 100
    
    global hbrake, hbrake_max, hbrake_min
    # Init values, do not change
    hbrake_max = int32_max * hbrake_inversion
    hbrake_min = int32_min * hbrake_inversion
    hbrake = hbrake_min
    
    global hbrake_increase_rate, hbrake_decrease_rate
    # Set hbrake behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    hbrake_increase_rate = calculate_rate(hbrake_max, hbrake_increase_time)
    hbrake_decrease_rate = calculate_rate(hbrake_max, hbrake_decrease_time) * -1        
    
    # =============================================================================================
    # Clutch settings
    # =============================================================================================   
    # In milliseconds
    clutch_increase_time = 0
    clutch_decrease_time = 50
    
    global clutch, clutch_max, clutch_min
    # Init values, do not change
    clutch_max = int32_max * clutch_inversion
    clutch_min = int32_min * clutch_inversion
    clutch = clutch_min
    
    global clutch_increase_rate, clutch_decrease_rate
    # Set clutch behaviour with the increase and decrease time,
    # the actual increase and decrease rates are calculated automatically
    clutch_increase_rate = calculate_rate(clutch_max, clutch_increase_time)
    clutch_decrease_rate = calculate_rate(clutch_max, clutch_decrease_time) * -1

    global mouselock
    mouselock = False

# assign button
vJoy[0].setButton(0,int(keyboard.getKeyDown(Key.Q)))
vJoy[0].setButton(1,int(keyboard.getKeyDown(Key.E)))
vJoy[0].setButton(2,int(keyboard.getKeyDown(Key.Z)))
vJoy[0].setButton(3,int(keyboard.getKeyDown(Key.X)))
vJoy[0].setButton(4,int(keyboard.getKeyDown(Key.R)))
vJoy[0].setButton(5,int(keyboard.getKeyDown(Key.V)))
#vJoy[0].setButton(6,int(keyboard.getKeyDown(Key.T)))
#vJoy[0].setButton(7,int(keyboard.getKeyDown(Key.Y)))


toggle_mouselock = mouse.getPressed(3)




if toggle_mouselock:
	mouselock = not mouselock
if (mouselock):
	user32.SetCursorPos(960, 5000)

# =================================================================================================
# LOOP START
# =================================================================================================

# =================================================================================================
# Steering logic
# =================================================================================================
if steering > 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_max))
elif steering < 0:
    steering_center_reduction = sensitivity_center_reduction ** (1 - (steering / steering_min))

steering = steering + ((float(mouse.deltaX) * mouse_sensitivity) / steering_center_reduction)

if steering > steering_max:
    steering = steering_max
elif steering < steering_min:
    steering = steering_min

v.x = int(round(steering))

# =================================================================================================
# Clutch logic
# =================================================================================================
if keyboard.getKeyDown(Key.C):
 clutch = clutch + clutch_increase_rate
else:
    clutch = clutch + clutch_decrease_rate

if clutch > clutch_max * clutch_inversion:
    clutch = clutch_max * clutch_inversion
elif clutch < clutch_min * clutch_inversion:
    clutch = clutch_min * clutch_inversion

v.z = clutch

# =================================================================================================
# Throttle logic
# =================================================================================================
#if keyboard.getKeyDown(Key.K):
#	throttle_max = (int32_max * throttle_inversion) /3
#	brakeflippy = 1
#elif keyboard.getKeyDown(Key.J) and brakeflippy == 1:
#	throttle_max = throttle_max2
#	brakeflippy = 0


if keyboard.getKeyDown(Key.W):
    throttle = throttle + throttle_increase_rate
else:
 throttle = throttle + throttle_decrease_rate

if throttle > throttle_max * throttle_inversion:
    throttle = throttle_max * throttle_inversion
elif throttle < throttle_min * throttle_inversion:
    throttle = throttle_min * throttle_inversion

v.y = throttle

# =================================================================================================
# Braking logic
# =================================================================================================
#if keyboard.getPressed(Key.B):
#	if brakeflippy == 1:
#		brakeflippy = 0
#	else:
#		brakeflippy = 1


#if brakeflippy == 1:
#	braking_max = braking_max / 2
#else:
#	braking_max = braking_max2
#if keyboard.getKeyDown(Key.B):
#	braking_max = braking_max / 2
#else:
#	braking_max = braking_max2

if keyboard.getKeyDown(Key.S):
    braking = braking + braking_increase_rate
else:
    braking = braking + braking_decrease_rate

if braking > braking_max * braking_inversion:
    braking = braking_max * braking_inversion
elif braking < braking_min * braking_inversion:
    braking = braking_min * braking_inversion

v.rz = braking

# =================================================================================================
# HandBraking logic
# =================================================================================================
if keyboard.getKeyDown(Key.Space):
    hbrake = hbrake + hbrake_increase_rate
else:
    hbrake = hbrake + hbrake_decrease_rate

if hbrake > hbrake_max * hbrake_inversion:
    hbrake = hbrake_max * hbrake_inversion
elif hbrake < hbrake_min * hbrake_inversion:
    hbrake = hbrake_min * hbrake_inversion

v.ry = hbrake


# =================================================================================================
# Buttons post-throttle logic
# ====================================================================﻿