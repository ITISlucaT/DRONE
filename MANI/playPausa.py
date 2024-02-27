import win32api

VK_MEDIA_PLAY_PAUSE = 0xB3
hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)
