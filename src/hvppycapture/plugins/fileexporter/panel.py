import logging

from PySide6.QtCore import Signal, Slot, QSettings
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLineEdit, QFileDialog
from hvppycapture.plugins.editor.editorpanel import GroupBoxEditorPanel
from hvppycapture.widgets.pixmapviewer import PixmapViewer

logger = logging.getLogger(__name__)


class FileExporter(GroupBoxEditorPanel):
    EXPORTPATH_KEY = "export_path"
    sig_save_requested = Signal(str)

    def __init__(self):
        GroupBoxEditorPanel.__init__(self, "Z.FileExporter")

        self.setTitle("Export")

        lyt = QHBoxLayout()
        self.setLayout(lyt)
        self.path_edit = QLineEdit()
        self.variable_button = QPushButton("Add Variable...")
        self.browse_button = QPushButton("Browse...")
        self.save_button = QPushButton("Save")
        lyt.addWidget(self.path_edit)
        # lyt.addWidget(self.variable_button)
        lyt.addWidget(self.browse_button)
        lyt.addWidget(self.save_button)

        self.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.save_enable(False)
        
        from hvppycapture.plugins.fileexporter.plugin import FileExporterPlugin
        settings: QSettings = QSettings()
        settings.beginGroup(FileExporterPlugin.NAME)
        path = settings.value(FileExporter.EXPORTPATH_KEY, "")
        settings.endGroup()
        self.path_edit.setText(path)

    def save_enable(self, enable):
        self.save_button.setEnabled(enable)

    @Slot()
    def on_browse_button_clicked(self):
        path, ext = QFileDialog.getSaveFileName(self, "Export")
        if path:
            self.path_edit.setText(path)

    @Slot()
    def on_save_button_clicked(self):
        if not self.path_edit.text():
            logger.warn("path not entered")
            return
        self.sig_save_requested.emit(self.path_edit.text())
        
        from hvppycapture.plugins.fileexporter.plugin import FileExporterPlugin
        settings: QSettings = QSettings()
        settings.beginGroup(FileExporterPlugin.NAME)
        settings.setValue(FileExporter.EXPORTPATH_KEY, self.path_edit.text())
        settings.endGroup()
