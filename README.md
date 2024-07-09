# Segmentation Application

## Description
This is a simple desktop application built with Python and Tkinter for petroglyphs detection and segmentation using YOLO.

## Requirements
- Python 3.x
- Ultralytics YOLO
- Pillow
- OpenCV
- Tkinter
- svgwrite
- shapely

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies using:
    ```bash
    pip install -r requirements.txt
    ```

## YOLOv9 Training
To train your YOLOv9 model, you need to organize your data into three main directories: `train`, `valid`, and `test`. Each of these directories must contain two subdirectories: `images` and `labels`.

## Directory Structure

Your directory structure should look like this:

data/

├── train/

│ ├── images/

│ │ ├── image1.jpg

│ │ ├── image2.jpg

│ │ └── ...

│ ├── labels/

│ │ ├── image1.txt

│ │ ├── image2.txt

│ │ └── ...

├── valid/

│ ├── images/

│ │ ├── image1.jpg

│ │ ├── image2.jpg

│ │ └── ...

│ ├── labels/

│ │ ├── image1.txt

│ │ ├── image2.txt

│ │ └── ...

├── test/

│ ├── images/

│ │ ├── image1.jpg

│ │ ├── image2.jpg

│ │ └── ...

│ ├── labels/

│ │ ├── image1.txt

│ │ ├── image2.txt

│ │ └── ...



### Images Directory

Each `images` directory should contain the images in JPEG format (`.jpg`).

### Labels Directory

Each `labels` directory should contain a corresponding text file (`.txt`) for each image. The text file should contain annotations for the objects in the image.

## Label Format

Each line in a label file represents one object and should follow this format:

0 <x1> <y1> ... <xn> <yn>

- `0`: This is the class ID. Since we want to segment only petroglyphs, the class ID is always 0.
- `<x1> <y1> ... <xn> <yn>`: These are the normalized coordinates of the object in the image. The coordinates should be in the range [0, 1].

### Example

For an image named `image1.jpg`, the corresponding label file `image1.txt` might look like this:

0 0.1 0.2 0.3 0.4 0.5 0.6

0 0.2 0.3 0.4 0.5 0.6 0.7

In this example, there are two objects annotated in the image, both belonging to class 0.

## Training the Model

Once your data is organized, you will need to modify the datav9.yaml file given in this repository. Then you can Simply run the script YOLOv9.py.
