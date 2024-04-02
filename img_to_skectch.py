import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import ImageTk, Image

class ImageToSketchConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Sketch Converter")
        self.root.geometry("1024x768")
        
        # Upload button
        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image, font=("Helvetica", 14))
        self.upload_button.pack(pady=10)

        # Line thickness slider
        self.line_thickness_slider = tk.Scale(self.root, label="Line Thickness", from_=1, to=10, orient="horizontal", command=self.update_preview, font=("Helvetica", 12))
        self.line_thickness_slider.pack()

        # Contrast slider
        self.contrast_slider = tk.Scale(self.root, label="Contrast", from_=0, to=2, resolution=0.1, orient="horizontal", command=self.update_preview, font=("Helvetica", 12))
        self.contrast_slider.pack()

        # Brightness slider
        self.brightness_slider = tk.Scale(self.root, label="Brightness", from_=-100, to=100, orient="horizontal", command=self.update_preview, font=("Helvetica", 12))
        self.brightness_slider.pack()

        # Preview frame
        self.preview_frame = tk.Frame(self.root, width=400, height=300)
        self.preview_frame.pack(pady=10)

        self.preview_label = tk.Label(self.preview_frame)
        self.preview_label.pack()

        # Save button
        self.save_button = tk.Button(self.root, text="Save Sketch", command=self.save_sketch, font=("Helvetica", 14))
        self.save_button.pack(pady=10)

        self.image_path = None
        self.original_image = None
        self.sketch_image = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg; *.jpeg; *.png")])
        if self.image_path:
            self.original_image = cv2.imread(self.image_path)
            if self.original_image is not None:
                self.update_preview()
                messagebox.showinfo("Success", "Image Uploaded Successfully!")
            else:
                messagebox.showerror("Error", "Failed to Load Image. Please Try Again.")

    def update_preview(self, event=None):
        if self.original_image is not None:
            line_thickness = self.line_thickness_slider.get()
            contrast = self.contrast_slider.get()
            brightness = self.brightness_slider.get()
            self.sketch_image = self.convert_to_sketch(self.original_image, line_thickness, contrast, brightness)
            self.update_preview_label()
        else:
            messagebox.showerror("Error", "Please Upload an Image First.")

    def update_preview_label(self):
        if self.sketch_image is not None:
            sketch_image_rgb = cv2.cvtColor(self.sketch_image, cv2.COLOR_BGR2RGB)
            sketch_image_pil = Image.fromarray(sketch_image_rgb).resize((400, 300))
            sketch_image_tk = ImageTk.PhotoImage(image=sketch_image_pil)
            self.preview_label.configure(image=sketch_image_tk)
            self.preview_label.image = sketch_image_tk
        else:
            self.preview_label.configure(image=None)

    def convert_to_sketch(self, image, line_thickness, contrast, brightness):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (7, 7), 0)
        inverted_blurred_image = 255 - blurred_image
        sketch_image = cv2.divide(gray_image, 255 - inverted_blurred_image, scale=256.0)
        sketch_image = cv2.multiply(sketch_image, contrast)
        sketch_image = cv2.add(sketch_image, brightness)
        sketch_image = cv2.GaussianBlur(sketch_image, (3, 3), 0)
        return cv2.cvtColor(sketch_image, cv2.COLOR_GRAY2BGR)

    def save_sketch(self):
        if self.sketch_image is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if save_path:
            # Extracting file extension from the save_path
            file_extension = save_path.split(".")[-1].lower()

            # Save as JPEG
            if file_extension == "jpg" or file_extension == "jpeg":
                cv2.imwrite(save_path, self.sketch_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
                messagebox.showinfo("Success", "Sketch Saved Successfully as JPEG!")

            # Save as PNG
            elif file_extension == "png":
                cv2.imwrite(save_path, self.sketch_image, [cv2.IMWRITE_PNG_COMPRESSION, 9])
                messagebox.showinfo("Success", "Sketch Saved Successfully as PNG!")

            # Invalid file type
            else:
                messagebox.showerror("Error", "Invalid file type. Please save as JPEG or PNG.")
        else:
         messagebox.showerror("Error", "Please Preview a Sketch First.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToSketchConverter(root)
    root.mainloop()
