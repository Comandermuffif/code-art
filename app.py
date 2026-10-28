"""code-art — a node-based generative art editor built on PyFlowGraph.

Run with:  python app.py

Nodes are Python functions (code-as-nodes). Color-mode nodes build real
``ColorMode`` objects and hand them downstream by reference; draw-mode nodes
sample a color mode and render it with Qt (QPainter/QImage) into an inline
preview. Graphs save/load as human-readable Markdown (.md).
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "vendor", "pyflowgraph", "src"))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QDockWidget, QMenu, QFileDialog,
)
from PySide6.QtGui import QAction, QKeySequence, QKeyEvent
from PySide6.QtCore import Qt

from core.node_graph import NodeGraph
from commands.node.batch_operations import DeleteMultipleCommand
from ui.editor.node_editor_view import NodeEditorView
from execution.graph_executor import GraphExecutor
from data.flow_format import load_flow_file, save_flow_file

import nodes as N


def delete_selected(graph) -> int:
    """Delete selected nodes and connections as a single undoable step.

    Uses the same DeleteMultipleCommand as the scene's built-in Delete-key
    handling, so nodes, edges, and groups all go in one undo unit.
    Returns the number of deleted items (0 if nothing was selected).
    """
    selected = graph.selectedItems()
    if not selected:
        return 0
    if graph.execute_command(DeleteMultipleCommand(graph, selected)):
        return len(selected)
    return 0


class CodeArtView(NodeEditorView):
    """NodeEditorView with Backspace deleting the current selection.

    Delete itself is already handled by the scene (NodeGraph.keyPressEvent).
    """

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Backspace and not event.modifiers():
            if delete_selected(self.scene()):
                event.accept()
                return
        super().keyPressEvent(event)


class CodeArtWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("code-art")
        self.setGeometry(80, 80, 1600, 1000)

        # Node editor scene + view.
        self.graph = NodeGraph(self)
        self.view = CodeArtView(self.graph, self)
        self.setCentralWidget(self.view)

        # Execution output log.
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        dock = QDockWidget("Output")
        dock.setWidget(self.output_log)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

        self.current_file: str | None = None
        self._build_menus()
        self._build_toolbar()

    # --- UI construction -----------------------------------------------------

    def _build_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self._action("&New", self.on_new, "Ctrl+N"))
        file_menu.addAction(self._action("&Load...", self.on_load, "Ctrl+O"))
        file_menu.addAction(self._action("&Save", self.on_save, "Ctrl+S"))
        file_menu.addAction(self._action("Save &As...", self.on_save_as, "Ctrl+Shift+S"))
        file_menu.addSeparator()
        file_menu.addAction(self._action("E&xit", self.close, "Ctrl+Q"))

        run_menu = menu_bar.addMenu("&Run")
        run_menu.addAction(self._action("&Execute Graph", self.execute_graph, "F5"))

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self._action("&Undo", self.graph.undo_last_command, "Ctrl+Z"))
        edit_menu.addAction(self._action("&Redo", self.graph.redo_last_command, "Ctrl+Shift+Z"))
        edit_menu.addSeparator()
        edit_menu.addAction(self._action("&Delete", self.on_delete, "Del"))

        # Nodes menu, grouped by category.
        nodes_menu = menu_bar.addMenu("&Nodes")
        for category, defs in N.node_defs_by_category().items():
            submenu = nodes_menu.addMenu(category)
            for node_def in defs:
                action = QAction(node_def.title, self)
                action.triggered.connect(
                    lambda checked=False, nd=node_def: self.add_node_def(nd))
                submenu.addAction(action)

    def _build_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.addAction(self._action("New", self.on_new))
        toolbar.addAction(self._action("Load", self.on_load))
        toolbar.addAction(self._action("Save", self.on_save))
        toolbar.addSeparator()
        toolbar.addAction(self._action("Execute", self.execute_graph, "F5"))

    def _action(self, text, slot, shortcut=None):
        action = QAction(text, self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    # --- Node creation -------------------------------------------------------

    def add_node_def(self, node_def: N.NodeDef, scene_pos=None):
        """Instantiate a node definition at the center of the view (or a point)."""
        if scene_pos is None:
            scene_pos = self.view.mapToScene(self.view.viewport().rect().center())
        return N.add_node(self.graph, node_def, pos=(scene_pos.x(), scene_pos.y()))

    def on_add_node(self, scene_pos=None):
        """Context-menu hook: pick a node type to add at the clicked point."""
        menu = QMenu(self)
        for category, defs in N.node_defs_by_category().items():
            submenu = menu.addMenu(category)
            for node_def in defs:
                action = submenu.addAction(node_def.title)
                action.triggered.connect(
                    lambda checked=False, nd=node_def, sp=scene_pos: self.add_node_def(nd, sp))
        menu.exec(self.mapToGlobal(self.view.mapFromScene(scene_pos)) if scene_pos else self.cursor().pos())

    # --- Deletion -----------------------------------------------------------

    def on_delete(self):
        """Delete the selected nodes/connections (Edit → Delete)."""
        deleted = delete_selected(self.graph)
        if deleted:
            self.output_log.append(f"Deleted {deleted} item(s)")

    # --- Execution -----------------------------------------------------------

    def execute_graph(self):
        self.output_log.clear()
        executor = GraphExecutor(
            self.graph, log_widget=self.output_log, venv_path_callback=lambda: None)
        executor.execute()

    # --- File operations -----------------------------------------------------

    def on_new(self):
        self.graph.clear_graph()
        self.current_file = None
        self.output_log.clear()

    def on_save(self):
        if self.current_file:
            save_flow_file(self.current_file, self.graph.serialize(),
                           title=os.path.basename(self.current_file))
            self.output_log.append(f"Saved: {self.current_file}")
        else:
            self.on_save_as()

    def on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Graph", "", "Markdown (*.md)")
        if not path:
            return
        if not path.lower().endswith(".md"):
            path += ".md"
        self.current_file = path
        self.on_save()

    def on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Graph", "", "Markdown (*.md)")
        if not path:
            return
        self.graph.clear_graph()
        self.graph.deserialize(load_flow_file(path))
        self.current_file = path
        self.output_log.append(f"Loaded: {path}")


def main():
    app = QApplication(sys.argv)
    window = CodeArtWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
