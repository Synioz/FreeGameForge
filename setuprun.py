import os
import pyautogui as py
from time import sleep as s


def setup(selectlanguage, mute, next):
    base_directory = os.getcwd()
    sub_directory = r'FreeGames\Games'
    directory_path = os.path.join(base_directory, sub_directory)
    setup_path = os.path.join(directory_path, 'setup.exe')
    permission = 581, 509
    selectlanguage = 693, 418 #default english
    mute = 461, 528
    next = 809, 534

    print(f"Searched file path: {setup_path}")
    os.path.exists(setup_path)
    if os.path.isfile(setup_path):
        print(f"setup.exe file found: {setup_path}")
        os.startfile(setup_path)
        s(10)
        # py.click(permission)
        py.press('left')
        py.press('enter')
        py.click(selectlanguage)
        py.click(mute)
        for i in range(4):
            py.click(next)
    else:
        print(f"setup.exe file does not exist: {setup_path}")
