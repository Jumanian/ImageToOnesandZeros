"""
Roblox Voxel Map Converter - Drag & Drop Version with Preview
Generates .txt files only
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageDraw
import os
import threading

class VoxelConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Voxel Map Converter")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image_path = None
        self.processing = False
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2b2b2b", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Roblox Voxel Map Converter",
            font=("Arial", 22, "bold"),
            bg="#2b2b2b",
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Convert country images to Roblox voxel maps",
            font=("Arial", 11),
            bg="#2b2b2b",
            fg="#aaaaaa"
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Controls container
        controls_container = tk.Frame(main_frame, bg="#f0f0f0")
        controls_container.pack(fill=tk.BOTH, expand=True)
        
        # Left side controls
        left_controls = tk.Frame(controls_container, bg="#f0f0f0")
        left_controls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right side output
        right_controls = tk.Frame(controls_container, bg="#f0f0f0")
        right_controls.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # File selection section
        file_frame = tk.LabelFrame(
            left_controls,
            text="Step 1: Select Your Image",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=20,
            pady=20
        )
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Drop zone
        drop_zone = tk.Frame(file_frame, bg="white", relief=tk.SUNKEN, bd=2, height=100)
        drop_zone.pack(fill=tk.X, pady=(0, 10))
        drop_zone.pack_propagate(False)
        
        self.drop_label = tk.Label(
            drop_zone,
            text="Drag & Drop Image Here",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#666"
        )
        self.drop_label.pack(expand=True)
        
        # Enable drag and drop on the drop zone
        drop_zone.drop_target_register(DND_FILES)
        drop_zone.dnd_bind('<<Drop>>', self.on_drop)
        
        # Browse button
        self.browse_btn = tk.Button(
            file_frame,
            text="Browse for Image File",
            font=("Arial", 13, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.browse_file,
            relief=tk.RAISED,
            bd=3
        )
        self.browse_btn.pack(fill=tk.X)
        
        # File info label
        self.file_info_label = tk.Label(
            file_frame,
            text="No file selected",
            font=("Arial", 10),
            bg="#f0f0f0",
            fg="#666",
            wraplength=550,
            justify=tk.LEFT
        )
        self.file_info_label.pack(pady=(15, 0))
        
        # Settings frame
        settings_frame = tk.LabelFrame(
            left_controls,
            text="Step 2: Adjust Settings",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=20,
            pady=20
        )
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Max dimension setting
        dim_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        dim_frame.pack(fill=tk.X, pady=8)
        
        dim_label_frame = tk.Frame(dim_frame, bg="#f0f0f0")
        dim_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            dim_label_frame,
            text="Map Size:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            dim_label_frame,
            text="(Lower = Faster, Higher = More Detail)",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        dim_control_frame = tk.Frame(dim_frame, bg="#f0f0f0")
        dim_control_frame.pack(fill=tk.X)
        
        self.dimension_var = tk.IntVar(value=100)
        
        tk.Label(
            dim_control_frame,
            text="Small (50)",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        ).pack(side=tk.LEFT)
        
        dimension_scale = tk.Scale(
            dim_control_frame,
            from_=20,
            to=300,
            orient=tk.HORIZONTAL,
            variable=self.dimension_var,
            bg="#f0f0f0",
            highlightthickness=0,
            length=350
        )
        dimension_scale.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            dim_control_frame,
            text="Large (300)",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        ).pack(side=tk.LEFT)
        
        self.dim_value_label = tk.Label(
            dim_control_frame,
            text="100",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            fg="#2196F3",
            width=5
        )
        self.dim_value_label.pack(side=tk.LEFT, padx=(10, 0))
        
        self.dimension_var.trace('w', lambda *args: self.dim_value_label.config(
            text=str(self.dimension_var.get())
        ))
        
        # Info text about black/white
        info_label = tk.Label(
            settings_frame,
            text="Black pixels = Land (Green) | White pixels = Water (Blue)",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666"
        )
        info_label.pack(pady=(10, 0))
        
        # Convert button frame
        convert_frame = tk.LabelFrame(
            left_controls,
            text="Step 3: Convert",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            padx=20,
            pady=20
        )
        convert_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.convert_btn = tk.Button(
            convert_frame,
            text="Convert to Roblox Format",
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.convert_image,
            state=tk.DISABLED,
            relief=tk.RAISED,
            bd=3
        )
        self.convert_btn.pack(fill=tk.X)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            convert_frame,
            mode='indeterminate',
            length=300
        )
        
        # Output text
        output_frame = tk.LabelFrame(
            right_controls,
            text="Output Log",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        text_frame = tk.Frame(output_frame, bg="#1e1e1e")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output_text = tk.Text(
            text_frame,
            height=12,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            padx=10,
            pady=10,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.output_text.yview)
        
        self.log("Ready! Drag and drop your image or click Browse.")
        self.log("Tip: Use a clear black and white image for best results!")
    
    def on_drop(self, event):
        """Handle drag and drop event"""
        file_path = event.data
        # Remove curly braces that tkinterdnd2 adds
        file_path = file_path.strip('{}').strip()
        self.load_image(file_path)
        
    def browse_file(self):
        """Open file browser"""
        file_path = filedialog.askopenfilename(
            title="Select Country Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """Load and validate image"""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found!")
            return
        
        try:
            # Test if it's a valid image
            img = Image.open(file_path)
            width, height = img.size
            img.close()
            
            self.image_path = file_path
            filename = os.path.basename(file_path)
            
            self.file_info_label.config(
                text=f"Selected: {filename}\nSize: {width}x{height} pixels",
                fg="#4CAF50"
            )
            
            self.drop_label.config(
                text=f"File loaded: {filename}",
                fg="#4CAF50"
            )
            
            self.convert_btn.config(state=tk.NORMAL)
            self.log(f"\nLoaded: {filename}")
            self.log(f"Original size: {width}x{height} pixels")
            self.log(f"Ready to convert! Click the convert button below.")
            
            # Generate preview
            self.generate_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid image file!\n\n{str(e)}")
            self.log(f"\n❌ ERROR: {str(e)}")
    
    def generate_preview(self):
        """Generate a preview of what the voxel map will look like"""
        if not self.image_path:
            return
        
        try:
            max_dim = self.dimension_var.get()
            threshold = 128  # Fixed threshold: black=land, white=water
            
            # Load and process image
            img = Image.open(self.image_path).convert('L')
            original_width, original_height = img.size
            
            # Resize if needed
            if original_width > max_dim or original_height > max_dim:
                ratio = min(max_dim / original_width, max_dim / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            width, height = img.size
            pixels = img.load()
            
            # Create preview image (color-coded)
            preview = Image.new('RGB', (width, height), (255, 255, 255))
            preview_pixels = preview.load()
            
            land_color = (34, 139, 34)  # Green for land
            water_color = (30, 144, 255)  # Blue for water
            
            for y in range(height):
                for x in range(width):
                    if pixels[x, y] < threshold:  # Inverted: darker = land
                        preview_pixels[x, y] = land_color  # Land
                    else:
                        preview_pixels[x, y] = water_color  # Water
            
            # Scale up for better visibility
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            if canvas_width <= 1:  # Canvas not yet drawn
                canvas_width = 1100
                canvas_height = 400
            
            scale_factor = min(canvas_width // width, canvas_height // height)
            if scale_factor < 1:
                scale_factor = 1
            display_width = width * scale_factor
            display_height = height * scale_factor
            preview = preview.resize((display_width, display_height), Image.Resampling.NEAREST)
            
            # Convert to PhotoImage for tkinter
            self.preview_image = ImageTk.PhotoImage(preview)
            
            # Display on canvas
            self.preview_canvas.delete("all")
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            if canvas_width <= 1:  # Canvas not yet drawn
                canvas_width = 1100
                canvas_height = 400
            
            x = (canvas_width - display_width) // 2
            y = (canvas_height - display_height) // 2
            
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.preview_image)
            self.preview_label.place_forget()
            
            self.log(f"Preview generated: {width}x{height} map")
            
        except Exception as e:
            self.log(f"Preview error: {str(e)}")
    
    def log(self, message):
        """Add message to output log"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def convert_image(self):
        """Convert image to Roblox data"""
        if not self.image_path or self.processing:
            return
        
        # Run conversion in separate thread to avoid freezing UI
        thread = threading.Thread(target=self.do_conversion, daemon=True)
        thread.start()
    
    def do_conversion(self):
        """Actual conversion logic"""
        self.processing = True
        
        # Update UI
        self.root.after(0, lambda: self.convert_btn.config(
            state=tk.DISABLED,
            text="Converting...",
            bg="#FF9800"
        ))
        self.root.after(0, lambda: self.browse_btn.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.progress.pack(pady=(15, 0)))
        self.root.after(0, lambda: self.progress.start(10))
        
        try:
            max_dim = self.dimension_var.get()
            threshold = 128  # Fixed threshold: black=land, white=water
            
            self.root.after(0, lambda: self.log(f"\n{'='*60}"))
            self.root.after(0, lambda: self.log("Starting conversion..."))
            self.root.after(0, lambda: self.log(f"Max dimension: {max_dim}"))
            
            # Open and process image
            img = Image.open(self.image_path).convert('L')
            original_width, original_height = img.size
            
            self.root.after(0, lambda: self.log(f"Original size: {original_width}x{original_height}"))
            
            # Resize if needed
            if original_width > max_dim or original_height > max_dim:
                ratio = min(max_dim / original_width, max_dim / original_height)
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.root.after(0, lambda: self.log(f"Resized to: {new_width}x{new_height}"))
            
            width, height = img.size
            pixels = img.load()
            
            # Generate Lua table
            output_dir = os.path.dirname(self.image_path)
            output_path = os.path.join(output_dir, "mapData.lua")
            
            self.root.after(0, lambda: self.log(f"Generating data..."))
            
            voxel_count = 0
            lua_table = "-- Auto-generated voxel map data\n"
            lua_table += f"-- Source: {os.path.basename(self.image_path)}\n"
            lua_table += f"-- Dimensions: {width}x{height}\n"
            lua_table += f"-- Generated by Roblox Voxel Map Converter\n\n"
            lua_table += "return {\n"
            
            for y in range(height):
                lua_table += "\t{"
                row_values = []
                for x in range(width):
                    value = 1 if pixels[x, y] < threshold else 0  # Inverted: darker = land (1)
                    row_values.append(str(value))
                    if value == 1:
                        voxel_count += 1
                lua_table += ",".join(row_values)
                lua_table += "},\n"
            
            lua_table += "}\n"
            
            # Write file
            with open(output_path, 'w') as f:
                f.write(lua_table)
            
            self.root.after(0, lambda: self.log(f"\n✅ SUCCESS!"))
            self.root.after(0, lambda: self.log(f"💾 Created: {output_path}"))
            self.root.after(0, lambda: self.log(f"📐 Final map size: {width}x{height}"))
            self.root.after(0, lambda: self.log(f"🧊 Total voxels: {voxel_count:,}"))
            self.root.after(0, lambda: self.log(f"{'='*60}"))
            self.root.after(0, lambda: self.log(f"\n📋 Next steps:"))
            self.root.after(0, lambda: self.log(f"1. Open Roblox Studio"))
            self.root.after(0, lambda: self.log(f"2. Create a ModuleScript in ReplicatedStorage"))
            self.root.after(0, lambda: self.log(f"3. Name it 'MapData'"))
            self.root.after(0, lambda: self.log(f"4. Copy the contents of mapData.lua into it"))
            self.root.after(0, lambda: self.log(f"5. Use the Roblox generator script!"))
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success!",
                f"Conversion complete!\n\n"
                f"Files saved to:\n{output_dir}\n\n"
                f"Created:\n"
                f"- mapData.txt (Copy into Roblox)\n"
                f"- mapPreview.png (Visual preview)\n\n"
                f"Map size: {width}x{height}\n"
                f"Voxels: {voxel_count:,}\n\n"
                f"Next: Copy mapData.txt into Roblox ModuleScript!"
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.log(f"\nERROR: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Conversion Failed", str(e)))
        
        finally:
            # Reset UI
            self.processing = False
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.progress.pack_forget())
            self.root.after(0, lambda: self.convert_btn.config(
                state=tk.NORMAL,
                text="Convert to Roblox Format",
                bg="#2196F3"
            ))
            self.root.after(0, lambda: self.browse_btn.config(state=tk.NORMAL))

def main():
    root = TkinterDnD.Tk()
    app = VoxelConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()