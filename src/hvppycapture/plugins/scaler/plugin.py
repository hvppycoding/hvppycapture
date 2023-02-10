from re import S
from typing import Optional
from hvppycapture.api.plugin import Plugin, Plugins
from hvppycapture.api.decorators import on_plugin_available
from hvppycapture.plugins.editor.plugin import EditorPlugin
from hvppycapture.plugins.scaler.panel import ScalerPanel


class ScalerPlugin(Plugin):
    NAME = "scaler"
    REQUIRES = [Plugins.Editor]

    def on_initialize(self):
        self._panel: Optional[ScalerPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)
        if not self._panel:
            self._panel = ScalerPanel()
        editor_plugin.add_panel(self._panel)
