import serial # pip install pyserial
import csv
import tkinter as tk # pip install tk
from tkinter import ttk

port='COM3'
baudrate=9600

def import_data():
    names_to_commands = {}
    commands_to_names = {}
    names_to_clears = {}
    with open('minidata.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # skip the header
        next(reader)
        for row in reader:
            name = row[0]
            command = row[1]
            clear = row[2]
            names_to_commands[name] = command
            commands_to_names[command] = name
            if len(clear) > 0:
                names_to_clears[name] = clear
                commands_to_names[clear] = f'clear {name}'
    return names_to_commands, commands_to_names, names_to_clears

names_to_commands, commands_to_names, names_to_clears = import_data()
unique_clear_commands = sorted(set(names_to_clears.values()))

def button_command(button):
    ascii_command = names_to_commands[button]
    print(button, ascii_command)
    send_ascii(ascii_command)

def send_ascii(ascii_command):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        ascii_command += '\r'
        #print(f"Sending {ascii_command}")
        ser.write(ascii_command.encode())
        #print(f"Sent: {ascii_command}")
        ser.close()
        command_label.config(text=ascii_command)
    except serial.SerialException as e:
        print(f"Serial error: {e}")

root = tk.Tk()
root.title('LED Tester - Mini')
root.geometry('1000x400')

switcher_delegates = ['MAIN', 'M/E 1', 'M/E 2', 'M/E 3', 'M/E 4']
sd_buttons = []
for c, sd_label in enumerate(switcher_delegates):
    new_button = ttk.Button(root, text=sd_label, command=lambda cmd=f"SWITCHER DELEGATE {sd_label}": button_command(cmd))
    new_button.config(width=6)
    new_button.grid(column=c+11, row=0)
    sd_buttons.append(new_button)

command_list = ['1','2','3','4','NET 1','NET 2','DDR 1','DDR 2','GFX','BLACK']
row_labels = ['FX/OVERLAY','PROGRAM','PREVIEW']
button_matrix = []
for i, row_label in enumerate(row_labels):
    button_list = []
    new_label = ttk.Label(root, text=row_label)
    new_label.grid(column=0, row=i+1)
    for j, command_label in enumerate(command_list):
        new_button = ttk.Button(root, text=command_label, command=lambda cmd=f"{row_label} {command_label}": button_command(cmd))
        new_button.config(width=6)
        new_button.grid(column=j+1, row=i+1)
        button_list.append(new_button)
    button_matrix.append(button_list)

def create_button(command_label, ascii_command, row, column):
    new_button = ttk.Button(root, text=command_label, command=lambda cmd=ascii_command: send_ascii(cmd))
    new_button.config(width=6)
    new_button.grid(column=column, row=row)
    return new_button

create_button('SHIFT', '15EF', 1, 14)
create_button('ALT', '15DF', 1, 15)
create_button('BKGD', '17AC', 1, 16)
create_button('DSK 1', '15BF', 1, 17)
create_button('DSK 2', '157F', 1, 18)
create_button('FTB', '176C', 1, 19)

create_button('TAKE', '13BF', 3, 16)
create_button('AUTO', '137F', 3, 17)

create_button('M/E 1', '14FB', 2, 11)
create_button('M/E 2', '14F7', 2, 12)
create_button('M/E 3', '14EF', 2, 13)
create_button('M/E 4', '14DF', 2, 14)
create_button('M/E 1', '13FB', 3, 11)
create_button('M/E 2', '13F7', 3, 12)
create_button('M/E 3', '13EF', 3, 13)
create_button('M/E 4', '13DF', 3, 14)

for k, clear_command in enumerate(unique_clear_commands):
    new_button = tk.Button(root, text=clear_command, command=lambda cmd=f"{clear_command}": send_ascii(cmd))
    new_button.config(width=4, bg='black', fg='white')
    new_button.grid(column=0, row=k+4)
    #button_matrix.append(new_button)

command_label = tk.Label(root, text='')
command_label.grid(column=19, row=5)

root.mainloop()
