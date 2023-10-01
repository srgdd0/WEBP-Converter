# WEBP-Converter
This tool is designed to convert images to the WebP format. It allows you to select a folder containing images, choose a folder for the converted images, set the conversion quality, and specify the number of threads for parallel processing.

## How to Compile

To create a standalone executable file that includes all the necessary dependencies, use the `PyInstaller` tool. Ensure that you have `PyInstaller` installed, and then run the following command in the command prompt:

```shell
pyinstaller --onefile main.py
```

After running this command, a single executable file will be created, which can be run on computers without Python installed.

## How It Works

The script performs the following actions:

1. It opens a graphical interface using the `tkinter` library, allowing you to select a folder containing images and a folder for the converted images.

2. After choosing the folders and setting conversion parameters (quality and the number of threads), it begins processing the images.

3. Images are processed in parallel using threads and converted to the WebP format with the specified quality.

4. Upon completing the conversion, a dialog box appears with information about the process's completion.

5. The interface allows you to choose various settings and control the conversion process.

This tool can be useful for converting a large number of images to the WebP format with customizable settings.
