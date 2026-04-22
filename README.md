Technologies Used
Python 3.11: Recommended version to ensure compatibility with MediaPipe binaries on Windows.

MediaPipe Pose: Used for robust body tracking, calculating the relationship between the nose position and the shoulder line.

OpenCV: Responsible for video capture and rendering real-time visual feedback elements.

Tkinter & Pillow: Used for the popup window interface and handling GIF frame animations.

Pygame: Manages the audio engine to execute persistent sound loops.

🛠️ How to Run
1. Environment Setup
Isolating dependencies is a best practice in Software Engineering. It is highly recommended to use a virtual environment:

Bash
# Create the environment
python -m venv .venv

# Activation (Windows)
.venv\Scripts\activate
2. Install Dependencies
Install all required libraries via the requirements file:

Bash
pip install -r requirements.txt
3. File Structure
Ensure your assets are organized according to the structure below so the code can correctly locate GIFs and audio files:

Plaintext
focus_booster/
├── assets/
│   ├── gif/                
│   │   ├── skeleton_war.gif
│   │   └── the_rock.gif
│   └── audios/
│       ├── skeleton.mp3
│       └── the_rock.mp3
├── main.py
└── requirements.txt
4. Execution
Start the monitoring system by running the main script:

Bash
python main.py
