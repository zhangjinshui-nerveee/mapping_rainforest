import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

class MapGalleryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Gallery App")

        # Variables
        self.map_filename = ""
        self.gallery_folder = ""

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Frame for the map
        self.map_frame = tk.Frame(self.root, width=400, height=400)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for the gallery
        self.gallery_frame = tk.Frame(self.root, width=400, height=400)
        self.gallery_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load Map button
        load_map_button = tk.Button(self.root, text="Load Map", command=self.load_map)
        load_map_button.pack(side=tk.TOP, pady=10)

        # Load Gallery button
        load_gallery_button = tk.Button(self.root, text="Load Gallery", command=self.load_gallery)
        load_gallery_button.pack(side=tk.TOP, pady=10)

    def load_map(self):
        self.map_filename = filedialog.askopenfilename(title="Select Map File", filetypes=[("OBJ files", "*.obj")])
        if self.map_filename:
            self.display_map()

    def display_map(self):
        # Read OBJ file and extract coordinates
        vertices = []
        with open(self.map_filename, 'r') as obj_file:
            for line in obj_file:
                if line.startswith('v '):
                    vertex = list(map(float, line.strip().split()[1:]))
                    vertices.append(vertex)

        vertices = np.array(vertices)

        # Create 3D plot
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c='b', marker='o')

        # Display the map
        plt.show()

    def load_gallery(self):
        self.gallery_folder = filedialog.askdirectory(title="Select Gallery Folder")
        if self.gallery_folder:
            self.display_gallery()

    def display_gallery(self):
        # Get all JPEG files in the gallery folder
        image_files = [f for f in os.listdir(self.gallery_folder) if f.lower().endswith(('.jpg', '.jpeg', 'JPG'))]

        # Display each image in the gallery
        for image_file in image_files:
            image_path = os.path.join(self.gallery_folder, image_file)

            # Open and display the image
            img = Image.open(image_path)
            img.thumbnail((150, 150))
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(self.gallery_frame, image=img_tk)
            label.image = img_tk  # Keep a reference to the image to prevent garbage collection
            label.pack(side=tk.TOP, padx=10, pady=5)

            # Add click event to redirect image to the map (replace with your logic)
            label.bind("<Button-1>", lambda event, path=image_path: self.redirect_to_map(path))


    def redirect_to_map(self, image_path):
        # Implement your logic to redirect the image to the map
        # For demonstration, print the selected image path
        print(f"Redirecting image to map: {image_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MapGalleryApp(root)
    root.mainloop()

