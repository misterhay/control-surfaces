import serial # pip install pyserial

port='COM4'
baudrate=9600

max_x = 0
max_y = 0
min_x = 99999999
min_y = 99999999

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
                    #print(data[:3], data[3], data[4:-2], data[-2:])
                    if len(data) > 4:
                        if data[-6:] != '46460D':
                            prefix = data[:3]
                            set = data[3]
                            command = data[4:-2]
                            if len(command) > 4: # for the joysticks that send 8 byte codes
                                #print(bytes.fromhex(command[:4]), bytes.fromhex(command[4:]))
                                # also print the command in decimal
                                x = int(bytes.fromhex(command[:4]), 16)
                                y = int(bytes.fromhex(command[4:]), 16)
                                '''
                                if x > max_x:
                                    max_x = x
                                if y > max_y:
                                    max_y = y
                                if x < min_x:
                                    min_x = x
                                if y < min_y:
                                    min_y = y
                                print(x, y, 'x', min_x, max_x, 'y', min_y, max_y)
                                '''
                                # map the x values from 0 to 255 to the range of -1 to 1
                                x = (x / 255) * 2 - 1
                                #x = "{:.3f}".format(x)
                                # map the y values from 0 to 255 to the range of -1 to 1
                                y = (y / 255) * 2 - 1
                                #y = "{:.3f}".format(y)
                                '''
                                # if x is between 0.08 and 0.2 set it to 0
                                if 0.08 < float(x) < 0.7:
                                    x = 0
                                # if y is between -0.06 and 0.05 set it to 0
                                if -0.06 < float(y) < 0.05:
                                    y = 0
                                '''
                                print(set, f'x: {x}, y: {y}')
                                
                            else:
                                if prefix == '7E3' and int(set) > 3: # transition bar == 4
                                    print(set, int(bytes.fromhex(command), 16)) # 0 to 254
                                else:
                                    print(prefix, set, command)
                        #if data[-6:] == '46460D':
                            #print(f'button up {data}')
                        #    pass
                        #else:
                        #    print(data[:3], data[3], data[4:-2])
                    #print(f"Length of command: {len(buffer)} bytes")
                    else:
                        if data != '460D':
                            print(data[:2], data[2:])
                    buffer.clear()  # Clear buffer for next message
except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("Exiting...")
    exit()
