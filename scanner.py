import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
from datetime import datetime
import winsound   # Windows sound alert

class QRScanner:
    def __init__(self, callback):
        self.cap = None
        self.running = False
        self.callback = callback
        self.scanned_data = set()  # prevent duplicates

    def start(self, video_label):
        if self.running:
            return
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.video_label = video_label
        self.update_frame()

    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            for qr in decode(frame):
                data = qr.data.decode("utf-8")

                if data not in self.scanned_data:
                    self.scanned_data.add(data)

                    # 🔊 Sound alert
                    winsound.Beep(1000, 150)

                    # Save to file
                    self.save_to_file(data)

                    # Update GUI output
                    self.callback(data)

                x, y, w, h = qr.rect

                # 🎞️ Glow animation
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 204), 3)
                cv2.putText(
                    frame, "Scanning...",
                    (x, y - 12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 204),
                    2
                )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((540, 320))
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.video_label.after(10, self.update_frame)

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def save_to_file(self, data):
        with open("scanned_qr_codes.txt", "a") as file:
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{time}] {data}\n")
