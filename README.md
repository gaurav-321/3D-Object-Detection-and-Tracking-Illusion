# 3D Object Detection and Tracking Illusion 🎨🤖

✨ **Description:**  
This Python project implements a real-time 3D object detection and tracking system using a webcam, Pygame, and OpenGL. It detects and tracks a person's face in 3D space and renders a 3D object (a chair and a shelf) that moves to create an illusion.

🚀 **Features:**
- Real-time face detection
- Dynamic rendering of 3D objects based on detected positions
- Support for multiple detection methods (face, mask)
- Customizable scene setup

🛠️ **Installation:**  
To run this project, you need Python installed on your system. Additionally, install the required dependencies using pip:

```sh
pip install pygame opencv-python numpy
```

📦 **Usage:**  
### Running the Script

To execute the script, use the following command in your terminal:

```sh
python main.py [face|mask]
```

- `face`: Use face detection for position tracking (default).
- `mask`: Use mask detection for position tracking.

### Example Usage

For real-time face-based 3D object tracking:

```sh
python main.py face
```

For real-time mask-based 3D object tracking:

```sh
python main.py mask
```

🔧 **Configuration:**  
No specific configuration options or environment variables are required at this time. The script assumes default settings which can be overridden by command line arguments.

🧪 **Tests:**  
Testing is not available for this project at the moment.

📁 **Project Structure:**
```
3D-Object-Detection-and-Tracking-Illusion/
├── Meshes/
│   ├── ChairMesh.py
│   ├── Mesh.py
│   ├── ShelfMesh.py
│   └── SphereMesh.py
├── Textures/
├── main.py
└── mask.py
```

🙌 **Contributing:**  
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to include tests if applicable.

📄 **License:**  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by [gag3301v] 🌐