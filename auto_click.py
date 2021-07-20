from pynput.keyboard import Listener, Key, KeyCode
import pyautogui
import math
import time
import win32api, win32con



pyautogui.PAUSE = 1
pyautogui.FAILSFE = True
store = set()
 
HOT_KEYS = {
    'autoClick': set([ Key.alt_l] )
}
start = 0
lastX = 0
lastY = 0
def  click(x,y):

	win32api.SetCursorPos((x,y))

	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def autoClick():
    global start, lastX, lastY
    if not start :
        lastX, lastY = pyautogui.position()
    start += 1
    X, Y = pyautogui.position()
    num = math.sqrt(pow(lastX-X, 2)+pow(lastY-Y, 2))
    print(lastX, lastY, X, Y, num)
    
    if num >= 25 :
        click(X,Y)
        lastX, lastY = pyautogui.position()
 
def handleKeyPress( key ):
    global start
    store.add( key )
 
    for action, trigger in HOT_KEYS.items():
        CHECK = all([ True if triggerKey in store else False for triggerKey in trigger ])
 
        if CHECK:
            try:
                
                func = eval( action )
                if callable( func ):
                   func()
            except NameError as err:
                print( err )
        else :
             start = 0
def handleKeyRelease( key ):
    if key in store:
        store.remove( key )
        
    # 종료
    if key == Key.alt.f2:
        return False
 
with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()

