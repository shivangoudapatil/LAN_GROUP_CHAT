import tkinter as tk
import threading
import queue
from server_thread import server
from message_handler import new_message_handler
from network_scanner import scan_network

class GUIApp:

    def __init__(self, root):

        self.root = root
        self.root.title("LAN CHAT SERVER")
        self.root.configure(bg="#f5f0e1")

        self.message_text = tk.Text(self.root, font=("Helvetica", 13))
        self.message_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.input_entry = tk.Entry(self.root, bg="#aed6dc", font=("Helvetica", 16))
        self.input_entry.insert(0,"Enter your name")
        self.input_entry.pack(fill=tk.BOTH, padx=22, pady=7)
        self.input_entry.bind("<Return>", self.send_message)

        self.queue = queue.Queue()  # For thread-safe communication
        self.users = dict()
        self.msgs = dict()
        self.name = ""
        self.tm = 0
        self.port = 12001
        self.flag = True

        self.print_thread = threading.Thread(target=self.print_messages)
        self.print_thread.start()

    def print_messages(self):
        while True:
            try:
                message = self.queue.get(block=False)
                self.message_text.insert(tk.END, message + "\n")
                self.message_text.see(tk.END)  # Auto-scroll to the latest message
            except queue.Empty:
                pass

    def send_message(self, event):

        input_text = self.input_entry.get()
        
        if input_text:

            if self.flag:
                self.flag = False
                scan_network(self, input_text)

            else:
                new_message_handler(self, input_text)

            self.input_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()