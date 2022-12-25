# 3D Object Detection and Tracking Illusion
This project is a real-time 3D object detection and tracking system using a webcam and Pygame with OpenGL. It can detect and track a person's face in 3D space and render a 3D object (currently a chair and a shelf)that moves in such way that a illusion is created

## Dependencies
- Pygame
- OpenCV
- NumPy
- PIL
## How to Use
Clone the repository and navigate to the directory:
```
git clone https://github.com/USERNAME/REPO.git
cd REPO
```
Run the script with the desired webcam index (default is 1):
```
python main.py [WEBCAM_INDEX]
```
Position your face in front of the webcam so that it is detected by the system. The 3D object will be rendered behind you in real-time.
## Customization
You can customize the 3D object that is rendered by modifying the ChairMesh and shelfMesh classes in the MeshRenderer module. You can also adjust the position and orientation of the object by modifying the draw_object function in the main module.

## Acknowledgements
The face detection aspect of this project is based on the tutorial Real-time Face Detection using Haar Cascades by OpenCV. The 3D rendering aspect is based on the tutorial 3D Graphics with Pygame by Nerd Paradise.
