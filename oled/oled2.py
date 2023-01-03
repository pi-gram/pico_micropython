from machine import Pin, I2C
print("i2c init")
i2c=I2C(0,scl=Pin(17),sda=Pin(16),freq=200000)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

import adafruit_ssd1306

reset_pin = Pin(0) # any pin!
print("old init")
#oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin, addr=0x3d)  #might be different value
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3d)  #might be different value
print("about to do stuff")

# Clear display.
oled.fill(0)
oled.show()

