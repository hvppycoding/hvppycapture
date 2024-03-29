from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit
from hvppycapture.plugins.editor.editorpanel import GroupBoxEditorPanel
from hvppycapture.widgets.pixmapviewer import PixmapViewer


class ScalerPanel(GroupBoxEditorPanel):
    def __init__(self):
        GroupBoxEditorPanel.__init__(self, "B.Scaler")
        self.setTitle("Scale Image")
        self.setCheckable(True)
        lyt = QGridLayout()

        lyt.addWidget(QLabel("Width [px]:"), 0, 0)
        self.width_edit = QLineEdit()
        lyt.addWidget(self.width_edit, 0, 1)
        self.setLayout(lyt)
