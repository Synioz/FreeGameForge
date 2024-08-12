import serverinfo as s
import gamename as gn
import nameConverter as nc
from time import sleep
import downloader
import unarchiver as ua
import setuprun as sr

def main():
    nc.print_banner()
    s.Info()
    if s.checker == 0:
        print('Program is closing...')
        sleep(5)
        exit()
    game_name = nc.name()  
    while True:
            
            auto = int(input('Auto Setup[1/0]: '))
            if auto == 1 or auto == 0:
                if auto == 1:
                    screensize = str(input('Enter Screen Size(Example: 1920 1080):'))
                    if screensize == '1920 1080':
                        permission = 581, 509
                        selectlanguage = 693, 418 #default english
                        mute = 461, 528
                        next = 809, 534
                        break
                    elif screensize == '1366 768':
                        permission = 581, 509
                        selectlanguage = 693, 418 #default english
                        mute = 461, 528
                        next = 809, 534
                        break
                    else:
                        print('Select 1366 768 or 1920 1080')
                break
            else:
                print('Please 1(True), 0(False) select only one.')
    while True:
        answer = int(input(f'\n{gn.game_Name(game_name)}\nIs game correct?[1/0]: '))
        if answer == 1:
            print('Game is Downloading...')
            sleep(1)
            downloader.downloadLinks(game_name)
            ua.unarchive()
            break
        if auto == 1:
            sleep(10)
            sr.setup(permission, selectlanguage, mute, next)
            break
        elif answer == 0:
            print('Program is closing...')
            sleep(5)
            exit()
        else:
            print('Please 1(Correct), 0(Not Correct) select only one.')

main()
print('Program Closing...')
sleep(4)
