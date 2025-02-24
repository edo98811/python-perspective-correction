import tkinter as tk
from tkinter import Button, Canvas
from PIL import ImageTk
from image_class import ImageData

class ImageCropperApp:
    def __init__(self, root):
        """Initialize the main application."""
        self.root = root
        self.root.title("Perspective correction tool")

        # Create an ImageData instance
        self.image = ImageData()
        self.image.find_next_image()
        self.image.load_image()

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI with canvas and buttons."""
        # Clear previous UI

        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame for buttons (placed at the top)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Apply transformation button
        # Instruction label instead of "Apply Transform" button
        self.instruction_label = tk.Label(button_frame, text="Select the edges of the table points to continue... IMPORTANT: always start from same corner (lower left)", fg="grey", font=("Arial", 12, "bold"))
        self.instruction_label.pack(side="left", padx=10)

        # Reset selection button (hidden initially)
        self.reset_button = tk.Button(button_frame, text="Reset Selection", command=self.reset_transform)
        self.reset_button.pack(side="left", padx=10)
        self.reset_button.pack_forget()  # Hide initially

        # Save transformed image button (hidden initially)
        self.save_button = tk.Button(button_frame, text="Save Transformed Image", command=self.confirm_transform)
        self.save_button.pack(side="left", padx=10)
        self.save_button.pack_forget()  # Hide initially

        # Create a Canvas for displaying the image (below the buttons)
        self.canvas = tk.Canvas(self.root, width=1000, height=1000)

        # Display the loaded image
        if self.image.image:
            self.tk_img = ImageTk.PhotoImage(self.image.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        self.canvas.pack()

        # Bind mouse click for selecting points
        self.canvas.bind("<Button-1>", self.select_point)

    def select_point(self, event):
        """Handle point selection on the image."""
        if len(self.image.points) < 4:
            self.image.points.append((event.x, event.y))
            self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red")

        if len(self.image.points) == 4:
            self.apply_transform()
            self.show_transform_buttons()

    def show_transform_buttons(self):
        """Show Reset and Save buttons after selecting 4 points."""
        self.instruction_label.pack_forget()  # Hide "Apply Transform"
        self.reset_button.pack(side="left", padx=10)  # Show "Reset Selection"
        self.save_button.pack(side="left", padx=10)  # Show "Save Transformed Image"

        # Disable further point selection
        self.canvas.unbind("<Button-1>")

    def apply_transform(self):
        """Apply perspective transformation."""
        self.image.warp_perspective()

        if self.image.warped_image:
            self.tk_warped = ImageTk.PhotoImage(self.image.warped_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_warped)

    def confirm_transform(self):
        """Save the transformed image and load a new one."""
        self.image.save_image()
        self.image.find_next_image()
        self.image.load_image()
        self.setup_ui()

    def reset_transform(self):
        """Reset the transformation and selection."""
        self.image.reset_points()
        self.setup_ui()

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()
