from machine import ADC,Timer,Pin
import time
SOUND_SPEED = 343
adc = ADC(28)
trigger_pin = Pin(10, mode = Pin.OUT)
echo_pin = Pin(11, mode= Pin.IN)
timer = Timer()

def mycallback(t):
   #Send pulse
   trigger_pin.on()
   time.sleep_us(10)
   trigger_pin.toggle()
   time_pulse = machine.time_pulse_us(echo_pin, 1, 20000)/10^6
   print("Time:",time_pulse)
   distance = time_pulse * SOUND_SPEED / 2
   print("Distance:",distance)
   reading = adc.read_u16()
   print("ADC: ",reading)
   
timer.init( mode = Timer.PERIODIC , period=1000 , callback = mycallback )
