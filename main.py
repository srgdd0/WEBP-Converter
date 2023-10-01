import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
import threading

input_folder = ""
output_folder = ""

def convert_to_webp(input_image_path, output_image_path, quality):
    img = Image.open(input_image_path)
    img.save(output_image_path, 'webp', quality=quality)

def process_files(files, quality):
    for input_image_path in files:
        if input_image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            relative_path = os.path.relpath(input_image_path, input_folder)
            output_image_path = os.path.join(output_folder, relative_path)

            if not os.path.exists(os.path.dirname(output_image_path)):
                os.makedirs(os.path.dirname(output_image_path))

            output_image_path = os.path.splitext(output_image_path)[0] + '.webp'

            convert_to_webp(input_image_path, output_image_path, quality)
            print(f'Конвертировано: {input_image_path} -> {output_image_path}')

def disable_interface():
    input_folder_entry.config(state="disabled")
    input_folder_button.config(state="disabled")
    output_folder_entry.config(state="disabled")
    output_folder_button.config(state="disabled")
    quality_entry.config(state="disabled")
    num_threads_entry.config(state="disabled")
    convert_button.config(state="disabled")

def enable_interface():
    input_folder_entry.config(state="normal")
    input_folder_button.config(state="active")
    output_folder_entry.config(state="normal")
    output_folder_button.config(state="active")
    quality_entry.config(state="normal")
    num_threads_entry.config(state="normal")
    convert_button.config(state="active")

def browse_input_folder():
    global input_folder
    folder_path = filedialog.askdirectory()
    input_folder = folder_path
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_path)

def browse_output_folder():
    global output_folder
    folder_path = filedialog.askdirectory()
    output_folder = folder_path
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_path)

def start_conversion():
    quality = int(quality_entry.get())
    num_threads = int(num_threads_entry.get())

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_files = []
    for foldername, _, filenames in os.walk(input_folder):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            all_files.append(file_path)

    file_groups = [all_files[i:i + num_threads] for i in range(0, len(all_files), num_threads)]

    disable_interface()  # Disable the interface during conversion

    def convert_in_background():
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for file_group in file_groups:
                executor.submit(process_files, file_group, quality)
        messagebox.showinfo("Conversion", "Готово!")
        enable_interface()  # Enable the interface after conversion

    conversion_thread = threading.Thread(target=convert_in_background)
    conversion_thread.start()

window = tk.Tk()
window.title("Инструмент конвертации изображений")

frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

input_folder_label = tk.Label(frame, text="Папка с изображениями:")
input_folder_label.grid(row=0, column=0, sticky="w")
input_folder_entry = tk.Entry(frame)
input_folder_entry.grid(row=0, column=1)
input_folder_button = tk.Button(frame, text="Выбрать", command=browse_input_folder)
input_folder_button.grid(row=0, column=2)

output_folder_label = tk.Label(frame, text="Папка для конвертированных изображений:")
output_folder_label.grid(row=1, column=0, sticky="w")
output_folder_entry = tk.Entry(frame)
output_folder_entry.grid(row=1, column=1)
output_folder_button = tk.Button(frame, text="Выбрать", command=browse_output_folder)
output_folder_button.grid(row=1, column=2)

quality_label = tk.Label(frame, text="Качество (0-100):")
quality_label.grid(row=2, column=0, sticky="w")
quality_entry = tk.Entry(frame)
quality_entry.grid(row=2, column=1)
quality_entry.insert(0, "80")

num_threads_label = tk.Label(frame, text="Количество потоков:")
num_threads_label.grid(row=3, column=0, sticky="w")
num_threads_entry = tk.Entry(frame)
num_threads_entry.grid(row=3, column=1)
num_threads_entry.insert(0, "8")

convert_button = tk.Button(frame, text="Начать конвертацию", command=start_conversion)
convert_button.grid(row=4, columnspan=3, pady=10)

window.mainloop()
