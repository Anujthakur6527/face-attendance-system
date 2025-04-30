import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import pyttsx3

# Constants
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = f"attendance_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
speaker = pyttsx3.init()

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Face Attendance System")
        self.root.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.name_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Status: Idle")
        self.count_var = ctk.StringVar(value="Total Present: 0")

        self.setup_ui()

    def setup_ui(self):
        frame = ctk.CTkFrame(self.root, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        title = ctk.CTkLabel(frame, text="📸 Face Recognition Attendance", font=("Arial", 26, "bold"))
        title.pack(pady=20)

        input_frame = ctk.CTkFrame(frame)
        input_frame.pack(pady=10)

        ctk.CTkLabel(input_frame, text="Student Name:", font=("Arial", 16)).pack(side="left", padx=10)
        ctk.CTkEntry(input_frame, textvariable=self.name_var, width=250, font=("Arial", 14)).pack(side="left")

        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=30)

        ctk.CTkButton(btn_frame, text="📝 Register Face", width=200, command=self.register_face).pack(pady=10)
        ctk.CTkButton(btn_frame, text="✅ Mark Attendance", width=200, command=self.mark_attendance).pack(pady=10)
        ctk.CTkButton(btn_frame, text="📤 Export Attendance", width=200, command=self.export_excel).pack(pady=10)

        status_frame = ctk.CTkFrame(frame)
        status_frame.pack(pady=10)

        ctk.CTkLabel(status_frame, textvariable=self.status_var, font=("Arial", 14)).pack(side="left", padx=20)
        ctk.CTkLabel(status_frame, textvariable=self.count_var, font=("Arial", 14)).pack(side="left", padx=20)

    def speak(self, text):
        speaker.say(text)
        speaker.runAndWait()

    def register_face(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a student name.")
            return

        cap = cv2.VideoCapture(0)
        count = 0
        while count < 10:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                count += 1
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))
                cv2.imwrite(f"{KNOWN_FACES_DIR}/{name}_{count}.png", face_img)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Registering Face', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", f"Registered {count} face images for {name}.")

    def mark_attendance(self):
        model, labels = self.train_model()
        if model is None:
            return

        cap = cv2.VideoCapture(0)
        marked = set()
        try:
            df = pd.read_excel(ATTENDANCE_FILE)
        except:
            df = pd.DataFrame(columns=['Name', 'Date', 'Time'])

        end_time = datetime.now().timestamp() + 10
        while datetime.now().timestamp() < end_time:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (100, 100)).flatten().astype(np.float32) / 255.0
                ret, result, _, _ = model.findNearest(np.array([face]), k=1)
                name = labels[int(result[0][0])]

                already_marked = ((df['Name'] == name) & (df['Date'] == datetime.now().strftime('%Y-%m-%d'))).any()
                if name not in marked and not already_marked:
                    now = datetime.now()
                    df.loc[len(df)] = [name, now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')]
                    marked.add(name)
                    self.status_var.set(f"✔ {name} marked present")
                    self.count_var.set(f"Total Present: {len(df[df['Date'] == now.strftime('%Y-%m-%d')])}")
                    self.speak(f"Attendance marked for {name}")
                else:
                    self.status_var.set(f"⚠ {name} already marked")

                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Attendance Scanner', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        df.to_excel(ATTENDANCE_FILE, index=False)
        self.status_var.set("✅ Attendance session completed")

    def train_model(self):
        data, labels, names = [], [], []
        name_map = {}
        current_index = 0

        for fname in os.listdir(KNOWN_FACES_DIR):
            if fname.endswith('.png'):
                path = os.path.join(KNOWN_FACES_DIR, fname)
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                name = fname.split('_')[0]
                if name not in name_map:
                    name_map[name] = current_index
                    names.append(name)
                    current_index += 1
                vector = img.flatten().astype(np.float32) / 255.0
                data.append(vector)
                labels.append(name_map[name])

        if not data:
            messagebox.showerror("Error", "No registered faces found. Please register first.")
            return None, None

        model = cv2.ml.KNearest_create()
        model.train(np.array(data), cv2.ml.ROW_SAMPLE, np.array(labels))
        return model, names

    def export_excel(self):
        try:
            df = pd.read_excel(ATTENDANCE_FILE)
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx")],
                                                     title="Save Attendance Report")
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exported", f"Attendance report saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export file: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = AttendanceApp(root)
    root.mainloop()