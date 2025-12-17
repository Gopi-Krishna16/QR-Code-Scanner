import tkinter as tk
from tkinter import ttk
from scanner import QRScanner

class QRScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)

        self.scanner = QRScanner(self.update_output)
        self.create_ui()

    def create_ui(self):
        # Title
        tk.Label(
            self.root,
            text="📷 QR Code Scanner",
            font=("Segoe UI", 22, "bold"),
            bg="#1e1e2f",
            fg="#ffffff"
        ).pack(pady=15)

        container = tk.Frame(self.root, bg="#1e1e2f")
        container.pack(fill="both", expand=True, padx=20)

        # Camera Card
        cam_card = tk.Frame(container, bg="#2a2a40")
        cam_card.place(x=0, y=0, width=580, height=420)

        tk.Label(
            cam_card,
            text="Live Camera Feed",
            font=("Segoe UI", 14, "bold"),
            bg="#2a2a40",
            fg="#00ffcc"
        ).pack(pady=10)

        self.video_label = tk.Label(cam_card, bg="#000000")
        self.video_label.pack(padx=10, pady=10)

        # Output Card
        out_card = tk.Frame(container, bg="#2a2a40")
        out_card.place(x=600, y=0, width=260, height=420)

        tk.Label(
            out_card,
            text="Decoded Data",
            font=("Segoe UI", 14, "bold"),
            bg="#2a2a40",
            fg="#ffcc00"
        ).pack(pady=10)

        self.output_box = tk.Text(
            out_card,
            height=18,
            width=30,
            font=("Consolas", 11),
            bg="#111122",
            fg="#00ffcc",
            insertbackground="white",
            bd=0
        )
        self.output_box.pack(padx=10, pady=10)
        self.output_box.config(state="disabled")

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="▶ Start Scanner", command=self.start).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="⏹ Stop Scanner", command=self.stop).grid(row=0, column=1, padx=10)

    def start(self):
        self.scanner.start(self.video_label)

    def stop(self):
        self.scanner.stop()

    def update_output(self, data):
        self.output_box.config(state="normal")
        self.output_box.insert("end", f"{data}\n")
        self.output_box.see("end")
        self.output_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = QRScannerApp(root)
    root.mainloop()
