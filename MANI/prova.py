#installare pynput
from pynput.mouse import Listener, Button

def on_click(x, y, button, pressed):
    if button == Button.left:
        print(f'Il pulsante sinistro è stato {"premuto" if pressed else "rilasciato"}')

def on_scroll(x, y, dx, dy):
    print('Rotella del mouse scorre {}{}'.format(
        'giù' if dy < 0 else 'su',
        ' a destra' if dx > 0 else ' a sinistra' if dx < 0 else ''))

with Listener(on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
