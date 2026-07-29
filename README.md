# 🖱️ SmartCursor – Vision-Based Virtual Mouse Using MediaPipe and OpenCV

SmartCursor is an AI-powered, vision-based virtual mouse that enables users to control a computer using **hand gestures** instead of a traditional physical mouse.

The system uses a standard webcam to capture real-time video, **OpenCV** for image processing, and **MediaPipe** for accurate hand landmark detection and tracking. Recognized hand gestures are converted into computer actions such as cursor movement, clicking, dragging, and scrolling.

The project also includes a **virtual keyboard** and **gesture-based mathematical calculations**, providing a touch-free and interactive human-computer interface.

## ✨ Features

* 🖐️ Real-time hand detection and tracking
* 🖱️ Touchless cursor movement
* 👆 Gesture-based left and right clicking
* ✋ Scrolling using hand gestures
* 🤏 Drag-and-drop functionality
* ⌨️ On-screen virtual keyboard
* 🧮 Gesture-based mathematical calculations
* 📹 Real-time webcam-based interaction
* ♿ Improved accessibility for users who have difficulty using traditional input devices
* 💻 Low-cost solution requiring only a standard webcam

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – Image processing and computer vision
* **MediaPipe** – Hand detection and landmark tracking
* **PyAutoGUI** – Mouse and cursor automation
* **Pyperclip** – Clipboard operations
* **Webbrowser** – Browser interaction
* **NumPy** – Mathematical and numerical operations

## 🏗️ System Modules

### 1. Hand Detection

Uses MediaPipe to detect and track hand landmarks and identify the coordinates of fingers and joints.

### 2. Gesture Recognition

Analyzes finger positions and movements to identify specific gestures and convert them into commands.

### 3. Cursor Control

Maps recognized gestures to mouse operations such as cursor movement and clicking.

### 4. Virtual Keyboard

Provides an on-screen keyboard that allows users to type using hand gestures.

### 5. Mathematical Calculations

Uses the distance between hand landmarks, such as the thumb and index finger, to detect interactions and perform calculations.

### 6. Output Display

Displays the live webcam feed, hand landmarks, recognized gestures, typed text, and calculation results.

## ⚙️ How It Works

```text
Webcam
   ↓
Capture Real-Time Video
   ↓
OpenCV Image Processing
   ↓
MediaPipe Hand Detection
   ↓
Hand Landmark Detection
   ↓
Gesture Recognition
   ↓
Gesture-to-Action Mapping
   ↓
Cursor / Click / Drag / Scroll / Keyboard / Calculator
```

## 💻 Requirements

### Software Requirements

* Windows or Linux
* Python 3.x
* VS Code or PyCharm
* Webcam

### Hardware Requirements

* Laptop or Desktop
* Built-in or external webcam
* Minimum 4 GB RAM
* Intel i3 processor or equivalent

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AbdulAzeem18/SmartCursor.git
```

### 2. Navigate to the Project Directory

```bash
cd SmartCursor
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Project

```bash
python main.py
```

> **Note:** The main Python file may have a different name depending on your project structure. Replace `main.py` with the correct filename if required.

## 🎮 Gesture Controls

| Gesture                       | Action                       |
| ----------------------------- | ---------------------------- |
| ☝️ Index Finger Movement      | Move Cursor                  |
| 🤏 Thumb + Index Finger Pinch | Left Click / Select          |
| 🤏 Ring Finger Gesture        | Right Click                  |
| ✋ Five Fingers                | Scroll                       |
| 🤏 Thumb + Index Drag         | Drag and Drop                |
| 🖐️ Hand Gestures             | Virtual Keyboard Interaction |

## 🧪 Testing

The project was evaluated through different levels of testing:

* **Unit Testing** – Individual modules such as camera initialization, hand landmark detection, and coordinate calculations.
* **Integration Testing** – Verification of communication between hand detection, gesture recognition, and cursor control.
* **System Testing** – Evaluation of performance, latency, environmental robustness, and hardware compatibility.
* **Acceptance Testing** – Validation of user experience, accessibility, and touch-free interaction.

## 🎯 Advantages

* Provides a completely touch-free computer interaction method
* Reduces dependency on physical mouse hardware
* Uses an affordable standard webcam
* Provides real-time gesture recognition
* Can improve accessibility
* Can be extended with additional gestures and features

## 🔮 Future Enhancements

* Add more gestures for advanced computer control
* Support window switching and application control
* Improve gesture recognition under different lighting conditions
* Reduce cursor jitter and improve movement smoothness
* Enhance virtual keyboard speed and accuracy
* Integrate advanced machine learning models for improved gesture recognition

## 👨‍💻 Team

* **K. Nazeer Abdul Azeem**
* **S. Praneetha**
* **S. Mohammad Adil**
* **C. Tejeswar**

**Guided by:** Mrs. K. Sreedevi, Assistant Professor

**Department:** Computer Science and Engineering (AI & ML)
**Institution:** Sri Venkateswara College of Engineering, Tirupati

## 📜 License

This project is developed for educational and academic purposes. You are free to modify and improve the project for learning and research purposes.

---

⭐ If you find this project interesting, consider giving the repository a **star**!
