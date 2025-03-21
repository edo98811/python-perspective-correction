# Image Perspective Correction App

## Overview
This App is a Python-based tool that allows you to correct the perspective of images in a given directory. It ensures uniform cropping and resizing to standard dimensions.

## Installation
### Prerequisites
Ensure you have Python installed on your system. To check if Python is installed and determine its alias, run the following commands:

```sh
which python
which py
which python3
```

For most systems, the alias is `python3`.

### Setup
1. Create a virtual environment and install dependencies (instead of python3 use your alias):

   ```sh
   python3 -m venv venv
   . venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

2. Start the application:

   ```sh
   python app.py
   ```

## Usage
1. **Configure Source and Destination**
   - Open `source_folders.json`.
   - Add the path to the folder containing the source images.
   - Add the path to the destination folder where corrected images should be saved.

2. **Image Processing**
   - The app will prompt you to correct all images.
   - The images will be cropped, the perspective will be corrected and then they will be resized to `1000x1000` pixels with corrected aspect ratios.
   - The images will be saved in JPG format.

3. **Output**
   - Corrected images will be stored in the designated output folder.
   - Some images may appear slightly distorted due to aspect ratio adjustments, but this ensures a common coordinate system.
   - You should not change the name of the images in the new folder, the app opens on its own images until all have been corrected, and the two folders have the same content. If you are not happy with one of the corrected images just delete it from the destination folder and it will be promped again

## Notes
- Ensure all required dependencies are installed before running the app.
- Output images maintain a consistent resolution for uniformity (the aspect rations may be deformed).
