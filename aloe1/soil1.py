#used for CAPACITY soil sensors

from machine import ADC, Pin
import utime

soil = ADC(Pin(26))
min_moisture = 9500 #0
max_moisture = 18000 #65535
readDelay = 0.5
cf = 3.3 / 65535

while True:
    moisture = (max_moisture-soil.read_u16()) * 100 / (max_moisture - min_moisture)
    print("moisture: "+"%2.f" % moisture+ "% (adc %"+str(soil.read_u16())+")")
    reading = soil.read_u16() * cf
    print(reading)
    utime.sleep(readDelay)

#to get max_moisture
    #dry soil
    #insert sensor
    #run code
    #get highest value
    #set in code
#to get min_moisture
    #put sensor in empty glass
    #fill with water
    #run code
    #get lowest value
    #set in code

