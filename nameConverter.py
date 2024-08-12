import pyfiglet

def name():
    game = input("What is download game today?\nYou: ")
    m = ""
    for i in range(len(game)):
        if game[i] == " ":
            m = m + "-"
        else:
            m = m + game[i]
    return m

def print_banner():
    font = pyfiglet.Figlet(font='slant')
    banner = font.renderText('FreePlayForge')
    lines = banner.split('\n')
    max_length = max(len(line) for line in lines)
    border_top_bottom = '\\' * (max_length + 6)
    border_side = '\\' + ' ' * (max_length + 4) + '\\'
    print(border_top_bottom)
    for line in lines:
        print(f'\\  {line.ljust(max_length)}  \\')
    by_syniox = 'By Syniox'
    print(f'\\  {by_syniox.center(max_length)}  \\')
    print(border_side)
    print(border_top_bottom)
