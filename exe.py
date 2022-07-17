import socket
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

PORT = 30050
BUFFER_SIZE = 4096

class udpcmdtool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("udpcmdtool")
        self.state('zoomed')

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT,fill=tk.Y)

        self.select_cmd = tk.IntVar()
        self.select_cmd.set(1)
        self.cmd = [('DAIKIN_UDP/common/basic_info',0),('DAIKIN_UDP/debug/loglevel=v',1),('DAIKIN_UDP/debug/nodesrv',2)]

        for cmd_name,val in self.cmd:
            self.select = tk.Radiobutton(self.right_frame,
            text=cmd_name,
            value=val,
            variable=self.select_cmd,
            font=("Century",12))
            self.select.pack(side=tk.TOP,fill=tk.X)

        #self.check_select = tk.Button(self.right_frame,text="選択",command=self.check_click)
        #self.check_select.pack(side=tk.TOP,fill=tk.X)

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(side=tk.TOP,fill=tk.X)

        self.ip_entry = tk.Entry(self.top_frame,font=("Century",12))
        self.ip_entry.pack(side=tk.LEFT,fill=tk.X)

        self.send_btn = tk.Button(
            self.top_frame,
            text='送信',
            command=self.send_btn_clicked,
        )

        self.send_btn.pack(side=tk.LEFT)

        """
        self.select_ip = tk.IntVar()
        self.select_ip.set(1)
        self.ip_kind = [('Unicast',0),('Broadcast',1)]

        for i,val in self.ip_kind:
            self.ip_buttom = tk.Radiobutton(self.top_frame,
            text=i,
            value=val,
            variable=self.select_ip,
            font=("Century",12))
            self.ip_buttom.pack(side=tk.LEFT,fill=tk.X)

        """

        self.ip_entry.insert(tk.END,"192.168.127.1")

        self.text = ScrolledText(self)
        self.text.pack(side=tk.TOP,expand=True,fill=tk.BOTH)

        self.init_sock()

    def log(self,msg):
        self.text.insert(tk.END,msg,'\n')
        self.text.see(tk.END)

    def init_sock(self):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
            )
        """
        if self.select_ip == 1:
            self.sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_BROADCAST,
                1)
        """
    def send_btn_clicked(self):
        self.ip = str(self.ip_entry.get())
        msg = self.cmd[self.select_cmd.get()][0]
        self.msg = msg.encode()

        self.log(f"\nSend>>{self.ip}:{msg}\n")

        self.sock.sendto(self.msg,(self.ip,PORT))

        recv_data, recv_addr = self.sock.recvfrom(BUFFER_SIZE)
        recv_data = recv_data.decode()
        self.log(f"Recv<<{recv_addr[0]}:{recv_data}\n")



if __name__ == '__main__':
    udpcmdtool = udpcmdtool()
    udpcmdtool.mainloop()

