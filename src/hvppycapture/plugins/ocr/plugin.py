import logging
from typing import Optional
from hvppycapture.api.plugin import Plugin, Plugins
from hvppycapture.api.decorators import on_plugin_available
from hvppycapture.widgets.layoutbuilder import LayoutBuilder
from hvppycapture.plugins.editor.editorpanel import GroupBoxEditorPanel
from hvppycapture.plugins.editor.plugin import EditorPlugin
from hvppycapture.plugins.clipboardwatcher.plugin import ClipboardWatcherPlugin
from hvppycapture.plugins.ocr.engine import OcrEngine


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OcrPanel(GroupBoxEditorPanel):
    def __init__(self):
        GroupBoxEditorPanel.__init__(self, "C2.OCR")
        self.setTitle("OCR")


class OcrPlugin(Plugin):
    NAME = "ocr"
    REQUIRES = [Plugins.Editor, Plugins.ClipboardWatcher]

    def on_initialize(self):
        self._engine: Optional[OcrEngine] = OcrEngine()
        self._panel: Optional[OcrPanel] = OcrPanel()
        
    def before_mainwindow_visible(self):
        assert self._panel
        logger.debug(f"{__class__}.before_mainwindow_visible")
        layout_builder = LayoutBuilder()
        logger.debug(f"layout_builder1: {layout_builder}")
        self._engine.add_to_layout(layout_builder=layout_builder)
        logger.debug(f"layout_builder2: {layout_builder}")
        layout_builder.attach_to(self._panel)
        return super().before_mainwindow_visible()
    
    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)
        editor_plugin.add_panel(self._panel)

    @on_plugin_available(plugin=Plugins.ClipboardWatcher)
    def on_clipboard_plugin_available(self):
        logger.info("clipboard available!")
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(
            Plugins.ClipboardWatcher
        )
        clipboard_plugin.sig_clipboard_changed.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    def on_clipboard_changed(self):
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(
            Plugins.ClipboardWatcher
        )
        if clipboard_plugin.pixmap:
            self._engine.set_pixmap(clipboard_plugin.pixmap)
