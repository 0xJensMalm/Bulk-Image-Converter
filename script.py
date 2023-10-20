import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
import os

# Global variables
resize_dimensions = None
new_file_type = None
output_folder_path = None


def load_content_to_tree(folder_path, tree, log_content=True):
    # Clear any existing items in the tree
    for row in tree.get_children():
        tree.delete(row)

    total_size = 0  # Initialize total size to zero
    total_images = 0  # Initialize total image count to zero

    for filename in os.listdir(folder_path):
        # Assuming you're only working with image files for now
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            
            # Use PIL to get image dimensions and size
            with Image.open(file_path) as img:
                width, height = img.size
                dimensions = f"{width}x{height}"
                
            file_type = img.format
            file_size = os.path.getsize(file_path)
            
            # Add the file size to the total size and increase the image count
            total_size += file_size
            total_images += 1
            
            # Insert these details into the tree
            tree.insert("", "end", values=(filename, file_type, dimensions, file_size))
    
    # Convert total size to kilobytes and display in the log
    total_size_kb = total_size / 1024  # Convert bytes to kilobytes
    if log_content:
        append_to_log(f"Total images fetched: {total_images}")
        append_to_log(f"Total size of loaded files: {total_size_kb:.2f} KB")


def update_output_folder():
    global output_folder_path
    if output_folder_path:
        load_content_to_tree(output_folder_path, tree_output)


def load_folder_content():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)
        load_content_to_tree(folder_path, tree_original)

def load_output_folder_content():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder.delete(0, tk.END)
        output_folder.insert(0, folder_path)
        load_content_to_tree(folder_path, tree_output)

def select_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    update_output_folder()


def on_resize_selected():
    global resize_dimensions
    width = int(entry_width.get())
    height = int(entry_height.get())
    resize_dimensions = (width, height)


def on_file_type_selected(event=None):
    global new_file_type
    new_file_type = dropdown_file_type.get()


def create_new_output_folder():
    # Get the current directory from the original path entry
    original_folder_path = path_entry.get()
    new_output_folder_path = os.path.join(original_folder_path, "output")
    
    # Create the new folder if it doesn't exist
    if not os.path.exists(new_output_folder_path):
        os.mkdir(new_output_folder_path)
    
    # Set the new output folder path to the output entry and tree view
    output_folder.delete(0, tk.END)
    output_folder.insert(0, new_output_folder_path)
    load_content_to_tree(new_output_folder_path, tree_output)

    append_to_log(f"Added new folder {new_output_folder_path}")
    load_content_to_tree(new_output_folder_path, tree_output, log_content=False)


def append_to_log(log_msg):
    log_display.configure(state='normal')  # Temporarily enable the widget to edit it
    log_display.insert(tk.END, log_msg + '\n')  # Append the log message
    log_display.see(tk.END)  # Scroll to the end
    log_display.configure(state='disabled')  # Disable the widget again



root = tk.Tk()
root.title("Bulk Image Editor")
mode = tk.StringVar()  # To store the selected mode

# Top bar
top_bar = tk.Frame(root, relief="groove", borderwidth=2)
top_bar.pack(side=tk.TOP, fill=tk.X, pady=5, padx=5)

title_label = tk.Label(top_bar, text="Bulk Image Editor", width=20, anchor=tk.W)
title_label.pack(side=tk.LEFT, padx=10)

ttk.Separator(top_bar, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=5)  # Section separator

path_entry = tk.Entry(top_bar, width=40)
path_entry.pack(side=tk.LEFT, padx=5)

btn_load_folder = tk.Button(top_bar, text="Load Folder Content", command=load_folder_content)
btn_load_folder.pack(side=tk.LEFT, padx=5)

ttk.Separator(top_bar, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=5)  # Section separator

single_mode_radio = tk.Radiobutton(top_bar, text="Single Mode", variable=mode, value="single")
single_mode_radio.pack(side=tk.LEFT, padx=5)    

bulk_mode_radio = tk.Radiobutton(top_bar, text="Bulk Mode", variable=mode, value="bulk")
bulk_mode_radio.pack(side=tk.LEFT, padx=5)

# Default mode to Single Mode
mode.set("single")

#  treeview
original_title_label = tk.Label(root, text="Original files")
original_title_label.pack(pady=2)
tree_original = ttk.Treeview(root, columns=("File", "Type", "Dimensions", "Size"), show="headings")
tree_original.heading("File", text="File")
tree_original.heading("Type", text="Type")
tree_original.heading("Dimensions", text="Dimensions")
tree_original.heading("Size", text="Size")
tree_original.pack(side=tk.TOP, pady=10)


# UI for dimensions and file type
edit_images_title_label = tk.Label(root, text="Edit image(s)")
edit_images_title_label.pack(pady=2)
controls_frame = tk.Frame(root)
controls_frame.pack(pady=5)

label_dimensions = tk.Label(controls_frame, text="Dimensions:")
label_dimensions.pack(side=tk.LEFT, padx=5)

entry_width = tk.Entry(controls_frame, width=5)
entry_width.pack(side=tk.LEFT, padx=2)

entry_height = tk.Entry(controls_frame, width=5)
entry_height.pack(side=tk.LEFT, padx=2)

btn_resize = tk.Button(controls_frame, text="Set", command=on_resize_selected)
btn_resize.pack(side=tk.LEFT, padx=5)

label_filetype = tk.Label(controls_frame, text="Filetype:")
label_filetype.pack(side=tk.LEFT, padx=5)

file_types = ["JPG", "PNG", "GIF", "BMP"]
dropdown_file_type = ttk.Combobox(controls_frame, values=file_types, width=5)
dropdown_file_type.pack(side=tk.LEFT, padx=5)
dropdown_file_type.bind("<<ComboboxSelected>>", on_file_type_selected)  

btn_convert = tk.Button(controls_frame, text="Convert")
btn_convert.pack(side=tk.LEFT, padx=5)  # Placed right next to the filetype selector

# Output folder display
output_label = tk.Label(root, text="Output Folder")
output_label.pack(pady=2)

output_frame = tk.Frame(root)
output_frame.pack(pady=5)

output_folder = tk.Entry(output_frame, width=50)
output_folder.pack(side=tk.LEFT, padx=5)

btn_output_folder = tk.Button(output_frame, text="Select Output Folder", command=select_output_folder)
btn_output_folder.pack(side=tk.LEFT, padx=5)

btn_new_output_folder = tk.Button(output_frame, text="New Output Folder", command=create_new_output_folder)
btn_new_output_folder.pack(side=tk.LEFT, padx=5)


tree_output = ttk.Treeview(root, columns=("File", "Type", "Dimensions", "Size"), show="headings")
tree_output.heading("File", text="File")
tree_output.heading("Type", text="Type")
tree_output.heading("Dimensions", text="Dimensions")
tree_output.heading("Size", text="Size")
tree_output.pack(side=tk.TOP, pady=10)


update_output_folder()

# Log display
log_label = tk.Label(root, text="Logs")
log_label.pack(pady=2)

log_display = tk.Text(root, height=5, width=60, bg='black', state='disabled')  # setting it to disabled to prevent manual edits
log_display.pack(pady=10, padx=10)


root.mainloop()
