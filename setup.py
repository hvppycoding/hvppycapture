from setuptools import setup, find_packages
import os

setup(
    name="pyclip2file",
    version="0.0.2",
    description="PyClip2File is a program that saves clipboard images to files.",
    author="hvppycoding",
    author_email="hvppycoding@gmail.com",
    packages=find_packages(),
    install_requires=[
        "PySide6",
    ],
    entry_points={
        "gui_scripts": ["pyclip2file = pyclip2file.app.start:main"],
        "pyclip2file.plugins": [
            "clipboard = pyclip2file.plugins.clipboard.plugin:ClipboardPlugin",
            "editor = pyclip2file.plugins.editor.plugin:EditorPlugin",
            "file_saver = pyclip2file.plugins.filesaver.plugin:FileSaverPlugin",
            "preview = pyclip2file.plugins.preview.plugin:PreviewPlugin",
            "scaler = pyclip2file.plugins.scaler.plugin:ScalerPlugin",
        ],
    },
)
