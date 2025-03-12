import serial # pip install pyserial

port='COM3'
baudrate=9600

print(f"Listening for Tricaster hex codes on {port}... (Press Ctrl+C to stop)")

try:
    with serial.Serial(port, baudrate, timeout=1) as ser:
        buffer = bytearray()
        while True:
            byte = ser.read(1)  # Read one byte at a time
            if byte:
                buffer.extend(byte)
                if byte.hex().upper() == '0D':  # Check for 0D hex code (carriage return)
                    data = buffer.hex().upper()
                    print(data)
                    if len(data) > 4:
                        if data[-6:] != '46460D':
                            prefix = data[:3]
                            set = data[3]
                            command = data[4:-2]
                            if len(command) > 4: # for the joysticks that send 8 byte codes
                                x = int(bytes.fromhex(command[:4]), 16)
                                y = int(bytes.fromhex(command[4:]), 16)
                                print(set, f'x: {x}, y: {y}')
                                
                            else:
                                if prefix == '7E3' and int(set) > 3: # transition bar == 4
                                    print(set, int(bytes.fromhex(command), 16)) # 0 to 254
                                else:
                                    print(prefix, set, command)
                    else:
                        if data != '460D':
                            print(data[:2], data[2:])
                    buffer.clear()  # Clear buffer for next message
except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("Exiting...")
    exit()
