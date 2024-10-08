import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess
import tempfile
import PyInstaller.__main__
import base64

# Function to combine EXEs
def combine_exes():
    exe1 = exe1_path.get()
    exe2 = exe2_path.get()
    icon_choice = icon_var.get()
    custom_icon = custom_icon_path.get()

    if not exe1 or not exe2:
        messagebox.showerror("Error", "Please select both EXE files")
        return

    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if not output_dir:
        return

    # Determine which icon to use
    if icon_choice == 1:
        icon_path = exe1
    elif icon_choice == 2:
        icon_path = exe2
    elif icon_choice == 3 and custom_icon:
        icon_path = custom_icon
    else:
        messagebox.showerror("Error", "Please choose a valid icon")
        return

    combined_script = os.path.join(output_dir, "combined_exe.py")

    # Read and encode the EXE files
    with open(exe1, 'rb') as f:
        exe1_data_b64 = base64.b64encode(f.read()).decode('utf-8')
    with open(exe2, 'rb') as f:
        exe2_data_b64 = base64.b64encode(f.read()).decode('utf-8')

    # Generate the Python script to extract and run both EXEs
    with open(combined_script, "w") as f:
        f.write(f"""import os
import subprocess
import sys
import tempfile
import base64

def extract_and_run(exe_data_b64, filename):
    temp_dir = tempfile.mkdtemp()
    exe_path = os.path.join(temp_dir, filename)
    exe_data = base64.b64decode(exe_data_b64.encode('utf-8'))
    with open(exe_path, 'wb') as exe_file:
        exe_file.write(exe_data)
    subprocess.Popen([exe_path])

def main():
    # Embedding EXE1
    exe1_data_b64 = \"\"\"{exe1_data_b64}\"\"\"
    extract_and_run(exe1_data_b64, "exe1.exe")

    # Embedding EXE2
    exe2_data_b64 = \"\"\"{exe2_data_b64}\"\"\"
    extract_and_run(exe2_data_b64, "exe2.exe")

if __name__ == "__main__":
    main()
""")

    # Use PyInstaller to create a single EXE
    PyInstaller.__main__.run([
        combined_script,
        '--onefile',
        '--icon=' + icon_path,
        '--name=combined_exe',
        '--distpath=' + output_dir
    ])

    # Clean up build files generated by PyInstaller
    build_dir = os.path.join(os.path.dirname(combined_script), 'build')
    spec_file = os.path.join(os.path.dirname(combined_script), 'combined_exe.spec')
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(spec_file):
        os.remove(spec_file)
    os.remove(combined_script)  # Remove the temporary combined_exe.py script

    messagebox.showinfo("Success", "EXEs combined successfully!")

# Function to browse EXE files
def browse_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])
    entry_widget.set(file_path)

# Function to browse for custom icon
def browse_icon():
    file_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    custom_icon_path.set(file_path)

# GUI Setup
root = tk.Tk()
root.title("EXE Combiner")

# Paths for the EXEs
exe1_path = tk.StringVar()
exe2_path = tk.StringVar()
custom_icon_path = tk.StringVar()
icon_var = tk.IntVar()

# EXE 1 selection
tk.Label(root, text="Select EXE 1").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=exe1_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: browse_file(exe1_path)).grid(row=0, column=2, padx=10, pady=10)

# EXE 2 selection
tk.Label(root, text="Select EXE 2").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=exe2_path, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=lambda: browse_file(exe2_path)).grid(row=1, column=2, padx=10, pady=10)

# Icon selection
tk.Label(root, text="Select Icon").grid(row=2, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="Use EXE 1 Icon", variable=icon_var, value=1).grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Use EXE 2 Icon", variable=icon_var, value=2).grid(row=3, column=1, sticky="w")
tk.Radiobutton(root, text="Use Custom Icon", variable=icon_var, value=3).grid(row=4, column=1, sticky="w")

# Custom icon selection
tk.Entry(root, textvariable=custom_icon_path, width=50).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Browse Icon", command=browse_icon).grid(row=5, column=2, padx=10, pady=10)

# Combine EXEs button
tk.Button(root, text="Combine EXEs", command=combine_exes).grid(row=6, column=1, padx=10, pady=20)

root.mainloop()
