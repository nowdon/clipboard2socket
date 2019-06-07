import sys
import socket
from time import sleep
import pyperclip
from tkinter import *
from tkinter import ttk
import tkinter
import threading

# -----------------------------------------------------------------------------

class MainWindow(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master.title('Clipboard to Socket')

        # create host entry
        self.host_lbl = Label(text='Host:')
        self.host_lbl.grid(row=0, sticky=W)
        self.host_box = Entry(width=20)
        self.host_box.insert(END, '127.0.0.1')
        self.host_box.grid(row=1, sticky=W)

        # create port entry
        self.port_lbl = Label(text='Port:')
        self.port_lbl.grid(row=2, sticky=W)
        self.port_box = Entry(width=20)
        self.port_box.insert(END, '62881')
        self.port_box.grid(row=3, sticky=W)

        # create clipboard text box
        self.cb_lbl = Label(text='Clipboard')
        self.cb_lbl.grid(row=6, sticky=W)
        self.cb_box = Text(width=40)
        self.cb_box.grid(row=7, rowspan=4, columnspan=2, sticky=NW)

        # create encoding combobox
        self.enc_lbl = Label(text='Encode:')
        self.enc_lbl.grid(row=4, sticky=W)
        self.enc_cmb = ttk.Combobox(master, state='readonly')
        self.enc_cmb['values'] = ('shift-jis', 'utf-8')
        self.enc_cmb.current(0)
        self.enc_cmb.grid(row=5, sticky=W)

        # Start clipboard monitoring in another thread
        self.t_stop = threading.Event()
        self.t = threading.Thread(target=getClipboard, args=(self,))
        self.t.start()

        # create send button
        self.send_btn = Button(master, text='send', command=self.onSendButton,
                                height=2, width=7)
        self.send_btn.grid(row=11, column=1, sticky=E)

    # send text data to host
    def onSendButton(self):
        host = self.host_box.get()
        port = int(self.port_box.get())
        text = self.cb_box.get('1.0', 'end -1c')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        if text is not None:
            s.sendall(text.encode(self.enc_cmb.get()))
        s.close()

    # close thread when window is closed
    def quitGUI(self):
        self.t_stop.set()
        while not self.t.is_alive():
            self.t.join(timeout=0.2)
        self.master.destroy()

def getClipboard(w):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')
    while not w.t_stop.is_set():
        box_current = w.cb_box.get('1.0', 'end -1c')
        clip_text = pyperclip.paste()
        # Replace out-of-range characters with empty characters
        clip_text = clip_text.translate(non_bmp_map)
        if clip_text == box_current:
            pass
        else:
            w.cb_box.delete('1.0', 'end')
            w.cb_box.insert('end', clip_text)
        sleep(0.5)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    root = tkinter.Tk()
    w = MainWindow(root)
    root.protocol("WM_DELETE_WINDOW", w.quitGUI)
    root.mainloop()