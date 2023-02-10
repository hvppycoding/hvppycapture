import logging
from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from hvppycapture.api.plugin import Plugin
from hvppycapture.api.decorators import on_plugin_available
from hvppycapture.api.plugin import Plugins
from hvppycapture.plugins.transformer.plugin import TransformerPlugin
from hvppycapture.plugins.editor.plugin import EditorPlugin
from hvppycapture.plugins.preview.panel import PreviewPanel

logger = logging.getLogger(__name__)


class PreviewPlugin(Plugin):
    NAME = "preview"
    REQUIRES = [Plugins.Transformer, Plugins.Editor]

    def on_initialize(self):
        self._pixmap: Optional[QPixmap] = None
        self._viewer: Optional[PreviewPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        logger.warn("editor available!")
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._viewer:
            self._viewer = PreviewPanel()
        if self._pixmap:
            self._viewer.setPixmap(self._pixmap)
        editor_plugin.add_panel(self._viewer)

    @on_plugin_available(plugin=Plugins.Transformer)
    def on_transformer_plugin_available(self):
        logger.warn("transformer available!")
        transformer_plugin: TransformerPlugin = self.get_plugin(Plugins.Transformer)
        transformer_plugin.sig_transformed_pixmap_changed.connect(
            self.on_transformed_pixmap_changed
        )
        self.on_transformed_pixmap_changed()

    @Slot()
    def on_transformed_pixmap_changed(self):
        transformer_plugin: TransformerPlugin = self.get_plugin(Plugins.Transformer)
        self._pixmap = transformer_plugin.transformed_pixmap()
        if self._pixmap and self._viewer:
            self._viewer.setPixmap(self._pixmap)
