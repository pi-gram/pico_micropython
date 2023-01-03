from machine import ADC, Pin, I2C
import utime

DELAY = 0.5

# use variables instead of numbers:
soil = ADC(Pin(26)) # Soil moisture PIN reference
#made up ranges - need to find correct values
SENSOR_MAX = 0
SENSOR_MIN = 9999

while True:
    # read moisture value and convert to percentage into the calibration range
    moisture = (SENSOR_MAX-soil.read_u16())*100/(SENSOR_MAX-SENSOR_MIN) 
    # print values
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    utime.sleep(DELAY) # set a delay between readings
    print("\n-------------------\n")
        