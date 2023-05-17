import sys
import time
from argparse import ArgumentParser
from bluepy import btle #linux

def main():
    while True:
        try:
            print("Connecting…")
            LODOWA_SENSOR = btle.Peripheral('40:91:51:9f:a9:22',) #mac address tutaj
        except:  
            print("Error: connecting")
            time.sleep(2)
            continue
        else:
            # time.sleep(2)
            # print("Connecting…")
            # LODOWA_SENSOR = btle.Peripheral('40:91:51:9f:a9:22') #mac address

            #reszzta kodu
            print("Discovering Services…")
            _ = LODOWA_SENSOR.services
            environmental_sensing_service = LODOWA_SENSOR.getServiceByUUID("181A")

            print("Discovering Characteristics…")
            _ = environmental_sensing_service.getCharacteristics()

            while True:
                print("\n")
                read_temperature(environmental_sensing_service)
                read_humidity(environmental_sensing_service)
                read_pressure(environmental_sensing_service)
                time.sleep(5) # transmission frequency
                
def byte_array_to_int(value):
    # Raw data is hexstring of int values, as a series of bytes, in little endian byte order
    # values are converted from bytes -> bytearray -> int
    # e.g., b'\xb8\x08\x00\x00' -> bytearray(b'\xb8\x08\x00\x00') -> 2232
    # print(f"{sys._getframe().f_code.co_name}: {value}")
    value = bytearray(value)
    value = int.from_bytes(value, byteorder="little")
    return value

def byte_array_to_char(value):
    # e.g., b'2660,2058,1787,4097\x00' -> 2659,2058,1785,4097
    value = value.decode("utf-8")
    return value

def pascals_to_hectopascals(value):
    return value / 100

def read_pressure(service):
    pressure_char = service.getCharacteristics("2A6D")[0]
    pressure = pressure_char.read()
    pressure = byte_array_to_int(pressure)/10
    pressure = pascals_to_hectopascals(pressure)
    print(f"Pressure: {round(pressure, 2)} hPa")

def read_humidity(service):
    humidity_char = service.getCharacteristics("2A6F")[0]
    humidity = humidity_char.read()
    humidity = byte_array_to_int(humidity)/100
    print(f"Humidity: {round(humidity, 2)}%")

def read_temperature(service):
    temperature_char = service.getCharacteristics("2A6E")[0]
    temperature = temperature_char.read()
    temperature = byte_array_to_int(temperature)/100
    print(f"Temperature: {round(temperature, 2)}°C")

if __name__ == "__main__":
    # main()
    while True:
        try:
            main()
            time.sleep(20)
        except:  
            print("Error main: probably the sensor disconnected")
            time.sleep(2)
            continue