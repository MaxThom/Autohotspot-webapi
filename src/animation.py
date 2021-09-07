from rpi_ws281x import Color, PixelStrip, ws
import time 

# LED strip configuration:
LED_COUNT = 144        # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
##LED_STRIP = ws.SK6812_STRIP_RGBW
LED_STRIP = ws.SK6812W_STRIP

def init_animation(logger):
    logger.info('> Starting LED animation...')
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    #luka_animation(strip)

    while True:
        # Color wipe animations.
        color_wipe(strip, Color(255, 0, 0))  # Red wipe
        color_wipe(strip, Color(0, 255, 0))  # Gree wipe
        color_wipe(strip, Color(0, 0, 255))  # Blue wipe
        color_wipe(strip, Color(0, 0, 0, 255))  # White wipe

def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def luka_animation(strip):
    strip.setPixelColor(0, Color(170, 0, 170, 0))
    strip.setPixelColor(1, Color(170, 0, 170, 0))
    strip.setPixelColor(2, Color(170, 0, 170, 0))

    strip.setPixelColor(4, Color(0, 50, 75, 0))
    strip.setPixelColor(5, Color(130, 25, 70, 0))
    strip.setPixelColor(6, Color(10, 255, 70, 200))

    strip.show()