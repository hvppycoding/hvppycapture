import sys
import logging
from typing import Optional
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from hvppycapture.api.registry import PLUGIN_REGISTRY
from hvppycapture.api.plugin import Plugin
from hvppycapture.app.find_plugins import find_plugins


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("hvppycapture")
        self.setup()

    def get_plugin(self, plugin_name: str) -> Plugin:
        if plugin_name in PLUGIN_REGISTRY:
            return PLUGIN_REGISTRY.get_plugin(plugin_name)
        else:
            raise Exception(f"Plugin {plugin_name} not found!")

    def setup(self) -> None:
        plugins = find_plugins()
        for plugin in list(plugins.values())[::-1]:
            logger.info(f"Registering Plugin: {plugin.NAME}")
            PLUGIN_REGISTRY.register_plugin(self, plugin)

    def pre_visible_setup(self):
        logger.info("Setting up window...")
        for plugin_name in PLUGIN_REGISTRY:
            plugin_instance = PLUGIN_REGISTRY.get_plugin(plugin_name)
            try:
                plugin_instance.before_mainwindow_visible()
            except AttributeError:
                pass


def setup_logger(filepath: str = "", use_stream: bool = True):
    from logging import FileHandler, StreamHandler

    fmt = "%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s"
    handlers = []
    if filepath:
        handlers.append(FileHandler(filepath, "w"))
    if use_stream:
        handlers.append(StreamHandler())

    logging.basicConfig(
        format=fmt,
        handlers=handlers,
    )


def main():
    setup_logger()
    app = QApplication()
    
    from hvppycapture import __author__
    app.setOrganizationName(__author__)
    
    from hvppycapture import __app_name__
    app.setApplicationName(__app_name__)
    
    from hvppycapture import __version__
    app.setApplicationVersion(__version__)
    
    mainwindow = MainWindow()
    mainwindow.pre_visible_setup()
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
