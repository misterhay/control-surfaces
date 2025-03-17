import serial # pip install pyserial
import time

port='COM3'
baudrate=9600

def send_ascii(ascii_command):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            ascii_command += '\r'
            ser.write(ascii_command.encode())
            print(f"Sent: {ascii_command}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")

prefixes = ['10','11','12','13','14','15','16','17','18','19']
suffixes = ['FE','FD','FB','F7','EF','DF','BF','7F','FF']
for prefix in prefixes:
    for suffix in suffixes:
        send_ascii(prefix + suffix)
        time.sleep(0.1)
