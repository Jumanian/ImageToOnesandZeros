"""
Roblox Voxel Map Converter
"""

import tkinter as tk
from tkinter import filedialog, messagebox
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except:
    HAS_DND = False
from PIL import Image
import os

class VoxelConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Voxel Map Converter")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")
        self.root.lift()  # Bring to front
        self.root.attributes('-topmost', True)  # Stay on top initially
        self.root.after(100, lambda: self.root.attributes('-topmost', False))  # Then allow normal behavior
        
        self.image_path = None
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        tk.Label(
            self.root,
            text="Voxel Map Converter",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        ).pack(pady=20)
        
        # Drop zone
        if HAS_DND:
            drop_frame = tk.Frame(self.root, bg="white", relief=tk.SUNKEN, bd=2, height=80)
            drop_frame.pack(pady=10, padx=40, fill=tk.X)
            drop_frame.pack_propagate(False)
            
            self.drop_label = tk.Label(
                drop_frame,
                text="Drag & Drop Image Here",
                font=("Arial", 12),
                bg="white",
                fg="#666"
            )
            self.drop_label.pack(expand=True)
            
            drop_frame.drop_target_register(DND_FILES)
            drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        
        # Browse button
        tk.Button(
            self.root,
            text="Select Image",
            font=("Arial", 12),
            command=self.browse_file,
            padx=20,
            pady=10
        ).pack(pady=10)
        
        # File label
        self.file_label = tk.Label(
            self.root,
            text="No file selected",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.file_label.pack(pady=10)
        
        # Map size
        tk.Label(
            self.root,
            text="Map Size:",
            font=("Arial", 10),
            bg="#f0f0f0"
        ).pack()
        
        self.size_var = tk.IntVar(value=100)
        tk.Scale(
            self.root,
            from_=20,
            to=300,
            orient=tk.HORIZONTAL,
            variable=self.size_var,
            bg="#f0f0f0"
        ).pack()
        
        # Convert button
        self.convert_btn = tk.Button(
            self.root,
            text="Convert",
            font=("Arial", 12, "bold"),
            command=self.convert,
            state=tk.DISABLED,
            padx=30,
            pady=10
        )
        self.convert_btn.pack(pady=20)
        
        # Status
        self.status = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        )
        self.status.pack(pady=10)
    
    def on_drop(self, event):
        file_path = event.data.strip('{}').strip()
        self.load_image(file_path)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        self.image_path = file_path
        filename = os.path.basename(file_path)
        self.file_label.config(text=filename)
        self.convert_btn.config(state=tk.NORMAL)
        if HAS_DND and hasattr(self, 'drop_label'):
            self.drop_label.config(text=f"Loaded: {filename}", fg="#4CAF50")
    
    def convert(self):
        if not self.image_path:
            return
        
        try:
            self.status.config(text="Converting...")
            self.root.update()
            
            # Load image
            img = Image.open(self.image_path).convert('L')
            max_size = self.size_var.get()
            
            # Resize if needed
            if img.width > max_size or img.height > max_size:
                ratio = min(max_size / img.width, max_size / img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            pixels = img.load()
            width, height = img.size
            
            # Generate data in Roblox format
            output = "-- Auto-generated voxel map data\n"
            output += f"-- Source: {os.path.basename(self.image_path)}\n"
            output += f"-- Dimensions: {width}x{height}\n\n"
            output += "return {\n"
            
            for y in range(height):
                output += "\t{"
                row = []
                for x in range(width):
                    row.append("1" if pixels[x, y] < 128 else "0")
                output += ",".join(row)
                output += "},\n"
            
            output += "}\n"
            
            # Save
            output_path = os.path.join(
                os.path.dirname(self.image_path),
                "mapData.txt"
            )
            
            with open(output_path, 'w') as f:
                f.write(output)
            
            self.status.config(text="Success!")
            messagebox.showinfo(
                "Done",
                f"Saved to:\n{output_path}\n\nSize: {width}x{height}"
            )
            
        except Exception as e:
            self.status.config(text="Error!")
            messagebox.showerror("Error", str(e))

def main():
    print("Starting application...")
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    print("Window created")
    app = VoxelConverter(root)
    print("App initialized - window should appear now")
    
    def on_close():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    print("Application closed")

if __name__ == "__main__":
    main()