# AI-Virtual-Painter-Pro
AI-powered hand gesture controlled virtual painting tool using Python, OpenCV, and MediaPipe.


# ✍️ AI Virtual Painter Pro

A high-performance virtual drawing tool that allows users to write and draw in the air using hand gestures. Powered by **Computer Vision**.

## 🚀 Features
- **Pinch-to-Draw**: Uses Euclidean distance between thumb and index finger for precise control.
- **Anti-Jitter Smoothing**: Implements Exponential Moving Average (EMA) for stable lines.
- **Auto-Shape Recognition**: Detects and fixes rough hand-drawn circles into perfect geometric shapes.
- **Gesture Commands**: Full palm gesture to clear the canvas.

## 🛠️ Tech Stack
- Python 3.x
- OpenCV (Image Processing)
- MediaPipe (Hand Landmark Detection)
- NumPy (Canvas Manipulation)

## 📦 Installation
1. Clone the repo: `https://github.com/Badalsha57/AI-Virtual-Painter-Pro`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python main.py`

## 🎮 How to Use
- **Pinch (Thumb + Index)**: Drawing mode.
- **Open Palm**: Eraser/Clear mode.
- **'q'**: Quit the application.
