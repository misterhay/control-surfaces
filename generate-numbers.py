import pyperclip
import pyautogui

prefix = '~9'
words = 'TRANSITION FX KNOB'

# make a list from 00 to FF
hex_list = [f'{i:02X}' for i in range(256)]
pyautogui.hotkey('alt', 'tab')
for i, hex_string in enumerate(hex_list):
    command = prefix + hex_string
    the_name = words + ' ' + str(i)
    print(the_name, command)
    pyperclip.copy(the_name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('right')
    pyperclip.copy(command)^F01F3
    pyautogui.hotkey('ctrl', 'v'A x:1 y:244)^F01F4
    pyautogui.press('down')
    pyautogui.press('left')
