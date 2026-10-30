"""Layer Images node: draw one image on top of another with adjustable opacity."""
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter

from nodes.base import NodeDef, Widget


def layer_images(base: QImage, overlay: QImage, opacity: float = 1.0) -> QImage:
    """Composite `overlay` over `base`, returning a new QImage the size of `base`.

    If the overlay is a different size it is scaled (stretching) to match the
    base. `opacity` is clamped to 0..1.
    """
    if base is None:
        raise ValueError("No base image - connect a draw node's image output")
    if overlay is None:
        raise ValueError("No overlay image - connect a draw node's image output")

    if overlay.size() != base.size():
        overlay = overlay.scaled(
            base.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    result = QImage(base.size(), QImage.Format.Format_ARGB32)
    result.fill(Qt.GlobalColor.transparent)

    painter = QPainter(result)
    try:
        painter.drawImage(0, 0, base)
        painter.setOpacity(max(0.0, min(1.0, opacity)))
        painter.drawImage(0, 0, overlay)
    finally:
        painter.end()
    return result


LAYER_IMAGES = NodeDef(
    title="Layer Images", category="Composite",
    code='''@node_entry
def layer_images(base: QImage = None, overlay: QImage = None, opacity: float = 1.0) -> QImage:
    """@outputs: image"""
    from nodes.composite.layer_images import layer_images as _layer_images
    return _layer_images(base, overlay, opacity)
''',
    widgets=[
        Widget("opacity", "float", 1.0, 0.0, 1.0),
    ],
    show_output=True,
)
