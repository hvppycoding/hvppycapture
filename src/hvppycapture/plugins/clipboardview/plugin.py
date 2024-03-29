import logging
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from hvppycapture.api.plugin import Plugin
from hvppycapture.api.decorators import on_plugin_available
from hvppycapture.api.plugin import Plugins
from hvppycapture.plugins.clipboardwatcher.plugin import ClipboardWatcherPlugin
from hvppycapture.plugins.editor.plugin import EditorPlugin
from hvppycapture.plugins.clipboardview.panel import ClipboardViewPanel

logger = logging.getLogger(__name__)


class ClipboardViewPlugin(Plugin):
    NAME = "clipboard_view"
    REQUIRES = [Plugins.ClipboardWatcher, Plugins.Editor]

    def on_initialize(self):
        self._pixmap: Optional[QPixmap] = None
        self._viewer: Optional[ClipboardViewPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._viewer:
            self._viewer = ClipboardViewPanel()
        if self._pixmap:
            self._viewer.setPixmap(self._pixmap)
        editor_plugin.add_panel(self._viewer)

    @on_plugin_available(plugin=Plugins.ClipboardWatcher)
    def on_clipboard_plugin_available(self):
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(
            Plugins.ClipboardWatcher
        )
        clipboard_plugin.sig_clipboard_changed.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @Slot()
    def on_clipboard_changed(self):
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(
            Plugins.ClipboardWatcher
        )
        self._pixmap = clipboard_plugin.pixmap
        if self._pixmap and self._viewer:
            self._viewer.setPixmap(self._pixmap)
