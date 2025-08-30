from machine import Pin,Timer

def blink_led(timer):
    led.toggle()
    

led = Pin( 25, Pin.OUT)
timer = Timer()
timer.init(mode = Timer.PERIODIC , period=1000 , callback = blink_led)
