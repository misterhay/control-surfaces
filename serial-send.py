import serial # pip install pyserial

port='COM3'
baudrate=9600

def send_hex(hex_command):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            command_bytes = bytes.fromhex(hex_command + '0D')
            ser.write(command_bytes)
            print(f"Sent: {hex_command + '0D'}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except ValueError:
        print("Invalid hex input.")

commands = [3746, 4246, 4446, 4546, 4637, 4642, 4644, 4645, 4646]
sets = [6, 2, 1]
for command in commands:
    for set in sets:
        if set == 6:
            n = 4
        else:
            n = 3
        hex_command = f"7e{n}{set}{command}"
        print(hex_command)
        send_hex(hex_command)