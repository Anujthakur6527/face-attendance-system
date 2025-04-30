# 📸 Fast Face Recognition Attendance System

A modern, real-time attendance system using face recognition built with Python, OpenCV, Tkinter (CustomTkinter), and Excel integration. The system allows students to register their faces and mark attendance automatically through a webcam interface.

---

## 🚀 Features

- 🎓 **Register Faces**: Capture and save multiple face images for a student.
- ✅ **Mark Attendance**: Automatically detects and identifies faces, marking attendance in real-time.
- 📦 **Export Attendance**: Save the daily attendance data to an Excel file.
- 🔊 **Voice Feedback**: Get audio confirmation when attendance is marked.
- 💡 **Modern GUI**: Built with `customtkinter` for a dark-mode-enabled and responsive interface.

---

## 🖥️ GUI Overview

- **Input Box**: Enter the student's name for registration.
- **Buttons**:
  - 📝 Register Face
  - ✅ Mark Attendance
  - 📤 Export Attendance
- **Live Webcam Feed** for both registration and attendance marking.
- **Status Bar** showing attendance updates and total present count.

---

## 🛠️ Tech Stack

- **Frontend (GUI)**: `customtkinter`, `Pillow`
- **Face Detection**: `OpenCV` with Haar Cascade
- **Machine Learning Model**: `cv2.ml.KNearest`
- **Data Storage**: `Pandas`, `.xlsx` Excel file
- **Voice Feedback**: `pyttsx3`

---

## 📂 Project Structure

```
📁 known_faces/              # Stores registered face images as PNGs
📄 attendance_YYYY-MM-DD.xlsx # Auto-generated attendance record file for each day
📄 app.py                   # Main Python script to launch the app
📄 README.md                # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Anujthakur6527/face-attendance-system.git
   cd face-attendance-system
   ```

2. **Install the required Python packages**:
   ```bash
   pip install opencv-python numpy pandas customtkinter pyttsx3 Pillow
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

---

## 🧪 How to Use

1. Enter a name in the input box and click **📝 Register Face**.
2. Let the webcam capture 10 face images (make sure your face is clearly visible).
3. Click **✅ Mark Attendance** to start recognizing and recording attendance.
4. To export the attendance, click **📤 Export Attendance** and save the `.xlsx` file.

---

## ❗ Notes

- Attendance data is saved automatically in an Excel file named `attendance_YYYY-MM-DD.xlsx`.
- Ensure your webcam is working properly.
- Run the program in a well-lit environment for better face detection accuracy.
- Face recognition uses simple KNN with grayscale pixel features. It's recommended to register clear, consistent facial images.

---

## 🧑‍💻 Author

**Anuj Thakur**  
🎓 B.Tech in Computer Science and Engineering  
🔗 [LinkedIn](#) | [GitHub](#)

---

