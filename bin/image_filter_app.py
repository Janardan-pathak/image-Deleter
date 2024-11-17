import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk


class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter")
        self.image_label = tk.Label(root)
        self.image_label.pack(expand=True)

        # Counter label to show the current image index
        self.counter_label = tk.Label(
            root, text="Image 1", font=("Arial", 16), anchor="center"
        )
        self.counter_label.pack(side=tk.TOP, pady=10)

        # Control buttons frame at the bottom
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        previous_button = tk.Button(
            button_frame, text="Previous", command=self.previous_image, width=12
        )
        previous_button.pack(side=tk.LEFT, padx=10, pady=10)

        keep_button = tk.Button(
            button_frame, text="Keep", command=self.keep_image, width=12
        )
        keep_button.pack(side=tk.LEFT, padx=10, pady=10)

        delete_button = tk.Button(
            button_frame, text="Delete", command=self.delete_image, width=12
        )
        delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        undo_button = tk.Button(
            button_frame, text="Undo", command=self.undo_image, width=12
        )
        undo_button.pack(side=tk.LEFT, padx=10, pady=10)

        next_button = tk.Button(
            button_frame, text="Next", command=self.next_image, width=12
        )
        next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Open folder dialog
        self.folder_path = filedialog.askdirectory(title="Select Folder with Images")
        if not self.folder_path:
            messagebox.showerror("Error", "No folder selected.")
            root.destroy()
            return

        # Load image files
        self.image_files = [
            f
            for f in os.listdir(self.folder_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
        ]
        self.current_image_index = 0
        self.deleted_images = []  # To store recently deleted images for undo

        if not self.image_files:
            messagebox.showerror("Error", "No images found in the selected folder.")
            root.destroy()
            return

        # Display the first image
        self.display_image()

    def display_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = os.path.join(
                self.folder_path, self.image_files[self.current_image_index]
            )
            image = Image.open(image_path)
            image.thumbnail((800, 600))  # Resize image to fit in the label
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)

            # Update the counter label with current image index and total images
            self.counter_label.config(
                text=f"Image {self.current_image_index + 1} of {len(self.image_files)}"
            )
        else:
            messagebox.showinfo("Completed", "No more images to review.")
            self.root.destroy()

    def keep_image(self):
        self.next_image()

    def delete_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = os.path.join(
                self.folder_path, self.image_files[self.current_image_index]
            )
            try:
                os.remove(image_path)
                self.deleted_images.append(
                    (
                        self.image_files[self.current_image_index],
                        self.current_image_index,
                    )
                )  # Save deleted image for undo
                del self.image_files[self.current_image_index]
                # Show the next image automatically after deletion
                self.display_image()
            except PermissionError:
                messagebox.showerror(
                    "Permission Denied",
                    "You do not have permission to delete this file.",
                )

    def undo_image(self):
        if self.deleted_images:
            last_deleted_image, index = self.deleted_images.pop()
            self.image_files.insert(index, last_deleted_image)
            self.current_image_index = index
            self.display_image()
        else:
            messagebox.showinfo("Undo", "No actions to undo.")

    def next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.display_image()
        else:
            messagebox.showinfo("End of List", "This is the last image.")

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_image()
        else:
            messagebox.showinfo("Start of List", "This is the first image.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
