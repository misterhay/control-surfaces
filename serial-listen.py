
import pyperclip # pip install pyperclip
import pyautogui # pip install pyautogui
import time

import serial # pip install pyserial

port='COM4'
baudrate=9600

print(f"Listening for Tricaster hex codes on {port}... (Press Ctrl+C to stop)")

over = True
try:
    with serial.Serial(port, baudrate, timeout=1) as ser:
        buffer = bytearray()
        while True:
            byte = ser.read(1)  # Read one byte at a time
            if byte:
                buffer.extend(byte)
                if byte == b'\r':
                    #print(buffer)
                    data = buffer[:-1].decode('ascii') # remove the last byte and decode
                    if data[:2] == '~F' or data[:2] == '~1' or data[:2] == '~2': # these buttons have two more bytes
                        extra_bytes = ser.read(2)
                        data += chr(extra_bytes[0])
                    print(data)
                    buffer.clear()
                    '''
                    if prefix == '~F' or prefix == '~1' or prefix == '~2':
                        # get the next byte
                        byte = ser.read(1)
                        buffer.extend(byte)
                        data = buffer.decode('ascii')
                        print(data)
                        buffer.clear()
                    else:
                        data = buffer.decode('ascii')
                        print(data)
                        buffer.clear()
                    #'''
                    '''
                    pyperclip.copy("'"+data)
                    pyautogui.hotkey('ctrl', 'v')
                    if over:
                        pyautogui.press('right')
                    else:
                        pyautogui.press('down')
                        pyautogui.press('left')
                    over = not over
                    #'''


except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("Exiting...")
    exit()