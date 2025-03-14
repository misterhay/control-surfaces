import pyperclip
import pyautogui


prefix = '~7'
words = 'OVERLAY TXT KNOB'

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
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('down')
    pyautogui.press('left')
