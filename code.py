import board
import neopixel
import time
import digitalio

# NeoPixel setup
pixels = neopixel.NeoPixel(board.GP7, 109, brightness=0.1, auto_write=False)    #set brightness depending on diffuser

# Button setup
button = digitalio.DigitalInOut(board.GP1)                                      #set soldered GPIO (button)
button.switch_to_input(pull=digitalio.Pull.UP)

# LED state variables
led_state = False
last_button_state = button.value
animation_active = False
current_color = (0, 0, 100)                                                     #set default color
color_options = [(0, 0, 100), (100, 0, 0), (0, 100, 0)]
color_index = 0

def initialize_neopixels():
    pixels.fill((0, 0, 0))
    pixels.show()
    return True

def run_animation():
    global animation_active, current_color
    animation_active = True
    
    number_of_leds = 109                                                        #set number of LEDs
    middle = number_of_leds // 2                                                
    duration = 0.1                                                              #set animation duration
    steps = middle
    delay = duration / steps
    
    for i in range(middle):
        # First half - light up from start
        pixels[i] = current_color
        # Second half - light up from end
        pixels[number_of_leds - i] = current_color
        pixels.show()
        time.sleep(delay)
    
    animation_active = False

if not initialize_neopixels():
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    while True:
        led.value = not led.value
        time.sleep(0.1)

while True:
    current_button_state = button.value
    
    if current_button_state != last_button_state:
        if not current_button_state:
            press_start_time = time.monotonic()
            
            while not button.value:
                time.sleep(0.01)
                if time.monotonic() - press_start_time > 1.0: 
                    color_index = (color_index + 1) % len(color_options)
                    current_color = color_options[color_index]
                    
                    if led_state:
                        pixels.fill(current_color)
                        pixels.show()
                    
                    while not button.value:
                        time.sleep(0.01)
                    break
            
            if time.monotonic() - press_start_time <= 1.0 and not animation_active:
                led_state = not led_state 
                
                if led_state:
                    run_animation()
                else:
                    pixels.fill((0, 0, 0))
                    pixels.show()
                
                time.sleep(0.2)
        
        last_button_state = current_button_state
    
    time.sleep(0.01)
