from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap
from hvppycapture.widgets.layoutbuilder import LayoutBuilder


class BaseTransformer(QObject):
    ID = None

    sig_updated = Signal()

    def __init__(self, parent: QObject = None):
        QObject.__init__(self, parent)

    def transform(self, pixmap: QPixmap) -> QPixmap:
        raise NotImplementedError()

    def add_to_layout(self, layout_builder: LayoutBuilder) -> LayoutBuilder:
        raise NotImplementedError()
