from machine import ADC,Timer,Pin
import time
adc = ADC(28)
n_samples=900
start = time.ticks_us()
SOUND_SPEED = 343
adc = ADC(28)
trigger_pin = Pin(10, Pin.OUT , Pin.PULL_DOWN)
echo_pin = Pin(11, Pin.IN , Pin.PULL_UP)
timer = Timer()
i=1
def mycallback(t):
   #Send pulse
   trigger_pin.on()
   time.sleep_us(20)
   trigger_pin.toggle()
   time_pulse = machine.time_pulse_us(echo_pin, 1, 1000000)/(10**6)
   print("Time:",time_pulse)
   distance = time_pulse * SOUND_SPEED / 2
   print("Start cycle ",i)
   samples=[]
   start=time.ticks_us()
   for j in range(n_samples):
        h = adc.read_u16()
        samples.append(h)
   end = time.ticks_us()
   time_elapsed= time.ticks_diff(end,start)
   print("Elapsed time:",time_elapsed)
   print("Samples:",samples)
timer.init( mode = Timer.PERIODIC , period=1000 , callback = mycallback )


    
    



