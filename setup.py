from setuptools import setup, find_packages
import os

setup(
    name="pyclip2file",
    version="0.0.3",
    description="PyClip2File is a program that saves clipboard images to files.",
    author="hvppycoding",
    author_email="hvppycoding@gmail.com",
    packages=find_packages(),
    install_requires=[
        "PySide6",
    ],
    entry_points={
        "console_scripts": ["pyclip2file = pyclip2file.app.start:main"],
        "pyclip2file.plugins": [
            'clipboard_view = pyclip2file.plugins.clipboardview.plugin:ClipboardViewPlugin',
            'clipboard_watcher = pyclip2file.plugins.clipboardwatcher.plugin:ClipboardWatcherPlugin',
            'editor = pyclip2file.plugins.editor.plugin:EditorPlugin',
            'file_exporter = pyclip2file.plugins.fileexporter.plugin:FileExporterPlugin',
            'postprocessor = pyclip2file.plugins.postprocessor.plugin:PostProcessorPlugin',
            'preview = pyclip2file.plugins.preview.plugin:PreviewPlugin',
            'scale_transformer = pyclip2file.plugins.scaletransformer.plugin:ScaleTransformerPlugin',
            'transformer = pyclip2file.plugins.transformer.plugin:TransformerPlugin',
        ],
    },
)
