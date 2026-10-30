"""Draw

Usage:
  gui.py [options]

Options:
  -h --help                   Show this screen
  -v --verbose                Print additional information

"""
from __future__ import annotations
import datetime
import itertools
import logging
import os

import docopt
import random
import string

from color_modes import ColorMode
from draw_modes import DrawMode

from modes import colorModeClasses, discover, drawModeClasses

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QImage, QKeySequence, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QScrollArea,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from models import FloatColor
from models.input import InputParser, InputEvaluator

POLL_INTERVAL_MS = 700


class DrawUI(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024

        self.inputFile = "input.conf"
        self.setWindowTitle("Code Art")
        self.resize(self.width + 120, self.height + 120)

        self.canvas = self._newCanvas()
        self.imagePrefix = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(8))
        self.imageCount = 0
        self._image: QPixmap | None = None

        self._buildToolbar()
        self._buildContents()
        self._clearImage()

        self.drawMode:DrawMode = None
        def SetDrawMode(drawMode:DrawMode):
            self.drawMode = drawMode

        self.colorMode:ColorMode = None
        def SetColorMode(colorMode:ColorMode):
            self.colorMode = colorMode

        def Draw():
            if not self.colorMode:
                logging.error("Color mode unset, unable to draw")
                self.statusBar().showMessage("Color mode unset, unable to draw")
                return

            if not self.drawMode:
                logging.error("Draw mode unset, unable to draw")
                self.statusBar().showMessage("Draw mode unset, unable to draw")
                return

            painter = QPainter(self.canvas)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            try:
                self.drawMode.draw(painter, self.colorMode, self.width, self.height)
            finally:
                painter.end()

        def parseTypes(input:str):
            if input.startswith("#") and (len(input) == 7 or len(input) == 9):
                return FloatColor.fromHex(input)

        # Import every colour/draw mode module once so their classes register
        # themselves with ColorMode/DrawMode.__subclasses__()
        discover()

        self.parser = InputEvaluator(
            itertools.chain(
                drawModeClasses(),
                colorModeClasses(),
                [
                    SetDrawMode,
                    SetColorMode,
                    Draw,
                    FloatColor.getSubcolors,
                    self._saveImage,
                ]
            ),
            parseTypes
        )

        self.inputModifiedTime:float = None
        self._inputMissing = False
        self._pollTimer = QTimer(self)
        self._pollTimer.timeout.connect(self._checkInput)
        self._pollTimer.start(0)

    # --- UI construction -------------------------------------------------

    def _buildToolbar(self) -> None:
        toolbar = QToolBar("Main", self)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.addToolBar(toolbar)

        generate = QAction("Generate", self)
        generate.setShortcut(QKeySequence("Ctrl+R"))
        generate.triggered.connect(self.draw)
        toolbar.addAction(generate)

        clear = QAction("Clear", self)
        clear.setShortcut(QKeySequence("Ctrl+L"))
        clear.triggered.connect(self._clearImage)
        toolbar.addAction(clear)

        save = QAction("Save", self)
        save.setShortcut(QKeySequence.Save)
        save.triggered.connect(self._saveImage)
        toolbar.addAction(save)

        toolbar.addSeparator()

        self.redraw = QAction("Redraw", self)
        self.redraw.setCheckable(True)
        self.redraw.setChecked(False)
        toolbar.addAction(self.redraw)

    def _buildContents(self) -> None:
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumSize(self.width // 4, self.height // 4)

        self.imageArea = QScrollArea()
        self.imageArea.setWidgetResizable(False)
        self.imageArea.setAlignment(Qt.AlignCenter)
        self.imageArea.setWidget(self.image)

        contents = QWidget()
        layout = QVBoxLayout(contents)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self.imageArea)
        self.setCentralWidget(contents)

    # --- Image handling --------------------------------------------------

    def _newCanvas(self) -> QImage:
        canvas = QImage(self.width, self.height, QImage.Format.Format_ARGB32_Premultiplied)
        canvas.fill(Qt.GlobalColor.transparent)
        return canvas

    def _clearImage(self):
        self.canvas = self._newCanvas()
        self._setImage()

    def _setImage(self):
        self._image = QPixmap.fromImage(self.canvas)
        self._showImage()

    def _showImage(self):
        if self._image is None:
            return

        scaled = self._image.scaled(
            self.imageArea.viewport().size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.image.setPixmap(scaled)
        self.image.resize(scaled.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._showImage()

    def _saveImage(self):
        os.makedirs("generated", exist_ok=True)
        path = f"generated/{self.imagePrefix}_{self.imageCount}.png"
        if not self.canvas.save(path):
            logging.error("Failed to save %s", path)
            self.statusBar().showMessage(f"Failed to save {path}")
            return

        self.imageCount += 1
        logging.info("Saved %s", path)
        self.statusBar().showMessage(f"Saved {path}")

    # --- Generation ------------------------------------------------------

    def draw(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            with open(self.inputFile, mode='r') as stream:
                tokens = InputParser.parse(stream)

            start_time = datetime.datetime.now()
            self.parser.parse(tokens)
            time_elapsed = datetime.datetime.now() - start_time
            logging.info("Draw took %f seconds", time_elapsed.total_seconds())

            self._setImage()
            self.statusBar().showMessage(f"Generated in {time_elapsed.total_seconds():.3f}s")
        except Exception as ex:
            logging.exception(ex)
            self.statusBar().showMessage(f"Draw failed: {ex}")
        finally:
            QApplication.restoreOverrideCursor()

    # --- Input file watching ---------------------------------------------

    def _checkInput(self) -> None:
        startTime = datetime.datetime.now()

        newModifiedTime = None
        try:
            newModifiedTime = os.path.getmtime(self.inputFile)
        except OSError:
            if not self._inputMissing:
                self._inputMissing = True
                logging.warning("Input file %s not found, waiting", self.inputFile)
                self.statusBar().showMessage(f"Waiting for {self.inputFile}")

        fileChanged = newModifiedTime is not None and (
            self.inputModifiedTime is None or newModifiedTime > self.inputModifiedTime
        )
        self.inputModifiedTime = newModifiedTime
        if newModifiedTime is not None:
            self._inputMissing = False

        if fileChanged or self.redraw.isChecked():
            self.draw()

        elapsedMs = (datetime.datetime.now() - startTime).total_seconds() * 1000
        self._pollTimer.start(max(int(POLL_INTERVAL_MS - elapsedMs), 1))


def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    logging.basicConfig(level=(logging.DEBUG if arguments['--verbose'] else logging.INFO))
    app = QApplication([])
    window = DrawUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()