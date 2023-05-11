import logging
from typing import Optional
from PySide6.QtCore import QObject
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *
from hvppycapture.widgets.layoutbuilder import LayoutItem, LayoutBuilder

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class OcrEngine(QObject):
    def __init__(self, parent: QObject = None) -> None:
        QObject.__init__(self, parent)
        self._pixmap: QPixmap = QPixmap()
        self._ocr_button: QPushButton = QPushButton("Run")
        self._ocr_button.clicked.connect(self.on_ocr_clicked)
        self._ocr_button.setEnabled(False)
        
        self._ocr_viewer: Optional[QPlainTextEdit] = QPlainTextEdit()
        self._ocr_viewer.setReadOnly(True)

    def add_to_layout(self, layout_builder: LayoutBuilder):
        layout_builder.add_space(1)
        layout_builder.add_widget(self._ocr_button)
        layout_builder.finish_row()
        layout_builder.add_widget(self._ocr_viewer, span=2)
        layout_builder.finish_row()
        
    def set_pixmap(self, pixmap: QPixmap):
        if not self._ocr_button.isEnabled():
            self._ocr_button.setEnabled(True)
        self._pixmap = pixmap
        
    def on_ocr_clicked(self):
        try:
            from PIL import Image
            import pytesseract
            image: Image = Image.fromqpixmap(self._pixmap)
            image = image.convert("L")
            text = pytesseract.image_to_string(image, lang="eng+kor")
            self._ocr_viewer.setPlainText(text)
        except Exception as e:
            logger.error(e)
            QMessageBox.critical(self._ocr_button, "OCR Error", str(e))