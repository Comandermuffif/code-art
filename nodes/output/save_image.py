"""Save Image node: write a rendered QImage to disk on execution."""
from nodes.base import NodeDef, Widget


SAVE_IMAGE = NodeDef(
    title="Save Image", category="Output",
    code='''@node_entry
def save_image(image: "QImage" = None, path: str = "output.png") -> "str":
    """@outputs: saved_path"""
    import os
    if image is None:
        raise ValueError("No image to save - connect a draw node's image output")
    if not path:
        raise ValueError("No output path set")
    path = os.path.abspath(os.path.expanduser(path))
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if not image.save(path):
        raise ValueError(f"Failed to save image (unsupported extension?): {path}")
    return path
''',
    widgets=[Widget("path", "file", "output.png")],
)
