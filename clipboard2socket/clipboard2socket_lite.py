__doc__ = """{f}

Usage:
    {f} <host> <port> [-e | --encode <encode>]
    {f} -h | --help

Options:
    -e --encode <encode>  encoding of the text to send to socket
    -h --help             Show this screen and exit.
""".format(f=__file__)

import sys
import socket
from time import sleep
from tkinter import *
from tkinter import ttk
import tkinter
import pyperclip
from docopt import docopt

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

        # create send button
        self.send_btn = Button(master, text='send', command=self.onSendButton,
                                height=5, width=10)
        self.send_btn.grid(row=0, column=1, rowspan=4, sticky=E)

        # create encoding combobox
        self.enc_lbl = Label(text='Encode:')
        self.enc_lbl.grid(row=4, sticky=W)
        self.enc_cmb = ttk.Combobox(master, state='readonly')
        self.enc_cmb['values'] = ('shift-jis', 'utf-8')
        self.enc_cmb.current(0)
        self.enc_cmb.grid(row=5, sticky=W)

    # send text data to host
    def onSendButton(self):
        h = self.host_box.get()
        p = int(self.port_box.get())
        e = self.enc_cmb.get()
        sendClipboard(h, p, e)

def sendClipboard(host, port, encode):
    text = pyperclip.paste()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    if text is not None:
        s.sendall(text.encode(encode))
    s.close()

def parseOpt():
    args = docopt(__doc__)
    h = str(args['<host>'])
    p = int(args['<port>'])
    if args['--encode']:
        e = str(args['--encode'][0])
    else:
        e = 'shift-jis'
    return h, p, e

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 2:
        root = tkinter.Tk()
        w = MainWindow(root)
        root.mainloop()
    else:
        host, port, encode = parseOpt()
        sendClipboard(host, port, encode)