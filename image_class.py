import os
import json
import cv2
import numpy as np
from PIL import Image, ImageTk
import pillow_heif
from pillow_heif import register_heif_opener

class ImageData:
    def __init__(self):
        """Initialize image data attributes."""
        self.image = None
        self.warped_image = None
        self.image_name = None
        self.image_path = None
        self.points = []
        self.source_folder = None
        self.destination_folder = None 

        register_heif_opener()
        self.find_folders()

    def load_image(self):
        """Load image from the current image path."""
        if not self.image_path:
            return
        
        heif_file = pillow_heif.open_heif(self.image_path)
        self.image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
        self.image.thumbnail((1000, 1000))  # Resize for display

    def save_image(self):
        """Save the transformed image, supporting HEIC format."""
        if self.warped_image and self.image_name:
            # Ensure destination folder exists
            os.makedirs(self.destination_folder, exist_ok=True)

            # Define save path
            save_path = os.path.join(self.destination_folder, self.image_name)

            # Check if saving as HEIC
            if self.image_name.lower().endswith(".heic"):
                save_path = os.path.join(self.destination_folder, self.image_name.replace(".heic", ".jpg"))
                self.warped_image = self.warped_image.convert("RGB")  # Convert to RGB for JPEG
                self.warped_image.save(save_path, format="JPEG", quality=95)  # Save as JPG
            else:
                self.warped_image.save(save_path)  # Default to standard formats

            print(f"Saved: {save_path}")

    def warp_perspective(self):
        """Apply a perspective transformation to the image using selected points (table edges)."""
        if len(self.points) != 4:
            print("Error: 4 points are required for warping.")
            return

        # Convert points to a NumPy array
        pts_src = self.reorder_points()
        print(pts_src)
        # pts_src = np.array(self.points, dtype=np.float32)

        # Compute the width and height dynamically based on input points
        width = int(max(np.linalg.norm(pts_src[1] - pts_src[0]), np.linalg.norm(pts_src[2] - pts_src[3])))
        height = int(max(np.linalg.norm(pts_src[2] - pts_src[1]), np.linalg.norm(pts_src[3] - pts_src[0])))

        # Define destination points for the top-down view
        pts_dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

        # Compute the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

        # Convert PIL image to OpenCV format (NumPy array)
        img_cv = np.array(self.image)

        # Apply perspective warp
        warped = cv2.warpPerspective(img_cv, matrix, (width, height))

        # Now resize the warped image to 1000x1000
        resized_warped = cv2.resize(warped, (800, 800))

        # Convert back to PIL image and store it
        self.warped_image = Image.fromarray(resized_warped)
        self.warped_image.thumbnail((1000, 1000)) 


    def find_folders(self):
        """Find the next image from the source folder."""
        with open('source_folders.json') as json_data:
            folders = json.load(json_data)

        self.source_folder = folders['source_folder']
        self.destination_folder = folders['destination_folder']

    def find_next_image(self):

        all_files = os.listdir(self.source_folder)
        all_destinations = os.listdir(self.destination_folder)

        for file_name in all_files:
            if file_name not in all_destinations:
                self.image_name = file_name
                self.image_path = os.path.join(self.source_folder, file_name)
                self.image = None
                self.warped_image = None
                self.points = []
                return

    def reset_points(self):
        """Reset the selected points."""
        self.points = []

    def reorder_points(self):
        """Reorders self.points to follow the order: 
        - (min x, min y) 
        - (max x, min y) 
        - (max x, max y) 
        - (min x, max y)
        """
        pts = np.array(self.points, dtype=np.float32)

        # Sort by y-coordinate first, then by x-coordinate
        pts = sorted(pts, key=lambda p: (p[1], p[0]))

        # (min x, min y)      (max x, min y)
        #     0 -------------- 1
        #     |                |
        #     |                |
        #     |                |
        #     |                |
        #     3 -------------- 2
        # (min x, max y)      (max x, max y)

        # Top-left (smallest y, then smallest x) 
        top_left = pts[0] if pts[0][0] < pts[1][0] else pts[1] # "take the first if the first is more on the left"
        # Top-right (smallest y, then largest x)
        top_right = pts[1] if pts[1][0] > pts[0][0] else pts[0] # "take the second if the second is more on the right"
        # Bottom-right (largest y, then largest x)
        bottom_right = pts[2] if pts[2][0] > pts[3][0] else pts[3] # "take the first if the first is more on the right"
        # Bottom-left (largest y, then smallest x)
        bottom_left = pts[3] if pts[3][0] < pts[2][0] else pts[2] # "take the second if the second is more on the left"

        # Reordered array
        return np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)