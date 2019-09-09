# Simple program for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import datetime

# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels =10 

# The order of the pixel colors - RGB or GRB. 
ORDER = neopixel.GRB


# Initialize
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER)

# Start & stop times for the lights
TOD_Start = 8 # Start at 8:00 am
TOD_Stop = 20 # Lights out at 8:00 pm

# Wheel is a subroutine to vary the colors
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

# rainbow cycles the colors on your strand of leds
# it calls wheel for different colors
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


# Finally the program
while True:
    currentTimeOfDay = datetime.datetime.now()
    currentHour = currentTimeOfDay.hour
    if ((currentHour >= TOD_Start) & (currentHour < TOD_Stop)):
        print ("Lights On!")
        rainbow_cycle(0.01)    # rainbow cycle with 1ms delay per step
    else:
        pixels.fill((0,0,0))
        pixels.show()
        print("Lights Out!")
        time.sleep(2)

