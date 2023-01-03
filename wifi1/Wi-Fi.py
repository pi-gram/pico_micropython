import network
import secrets
import time
import urequests
import machine
import utime
import ubinascii

led = machine.Pin("LED", machine.Pin.OUT)

if hasattr(network, "WLAN"):
   # the board has WLAN capabilities - therefore it is a Pico W
   wlan = network.WLAN(network.STA_IF)
   wlan.active(True)
   wlan.connect(secrets.SSID, secrets.PASSWORD)
   max_wait = 10
   while max_wait > 0:
       if wlan.status() < 0 or wlan.status() >= 3:
           break
       max_wait -= 1
       print("waiting for connection...")
       time.sleep(1)
   #handle connection error
   if wlan.status() != 3:
      raise RuntimeError("wifi comms failed")
   else:
      print("connected to WiFi = " + str(wlan.isconnected()))
      status = wlan.ifconfig()
      print("IP ADDR = " + status[0])
      mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
      print("MAC     = " +mac)
      print("CHANNEL = "+str(wlan.config('channel')))
      print("SSID    = "+str(wlan.config('essid')))
      print("TX PWR  = "+str(wlan.config('txpower')))
      #where is the ISS right now?
      iss = urequests.get("http://api.open-notify.org/iss-now.json").json()
      print("ISS is currently located at:"+iss['iss_position']['longitude']+","+iss['iss_position']['latitude'])
      #{"message": "success", "iss_position": {"longitude": "22.4391", "latitude": "40.6717"}, "timestamp": 1668960520}
      #fetch a list of astronauts currently in space from the internet
      print("These people are in SPACE atm:")
      astronauts = urequests.get("http://api.open-notify.org/astros.json").json()
      number = astronauts['number']
      for i in range(number):
         print(astronauts['people'][i]['name']+" - "+astronauts['people'][i]['craft'])
         led.value(1)
         utime.sleep(1)
         led.value(0)
         utime.sleep(1)
      #should flash LED when printing each name out
      