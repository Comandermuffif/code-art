# code-art demo

A generative-art flow ending in an image saved to disk.

## Node: Linear Gradient (ID: 15b8a312-abb4-4040-bfbf-2ccf8131a587)

### Metadata

```json
{
  "uuid": "15b8a312-abb4-4040-bfbf-2ccf8131a587",
  "title": "Linear Gradient",
  "pos": [
    -750.0,
    -150.0
  ],
  "size": [
    250,
    150
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {}
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def linear_gradient() -> ColorMode:
    from nodes.color.linear_gradient import LinearGradientColorMode
    return LinearGradientColorMode()

```

### GUI State Handler

```python
def get_values(widgets):
    return {}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    pass

```


## Node: Invert (ID: ba9f8e1f-0772-4a38-9747-bbdd4934d5ec)

### Metadata

```json
{
  "uuid": "ba9f8e1f-0772-4a38-9747-bbdd4934d5ec",
  "title": "Invert",
  "pos": [
    -500.0,
    -150.0
  ],
  "size": [
    281.15625,
    150
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {}
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def invert(child: ColorMode = None) -> ColorMode:
    from nodes.modify.invert import InvertColorMode
    return InvertColorMode(child)

```

### GUI State Handler

```python
def get_values(widgets):
    return {}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    pass

```


## Node: Draw Circles (ID: c1c2fd7b-d76e-483a-9098-2df704862a67)

### Metadata

```json
{
  "uuid": "c1c2fd7b-d76e-483a-9098-2df704862a67",
  "title": "Draw Circles",
  "pos": [
    -250.0,
    -150.0
  ],
  "size": [
    250,
    267
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "count": 300,
    "min_size": 2.0,
    "max_size": 20.0,
    "width": 512,
    "height": 512
  }
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def circles(field: ColorMode = None, count: int = 300, min_size: float = 2, max_size: float = 20, width: int = 512, height: int = 512) -> QImage:
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.circles import draw_circles
    return render_to_qimage(field, draw_circles, width, height, count=count, min_size=min_size, max_size=max_size)

```

### GUI Definition

```python
widgets['count'] = QtWidgets.QSpinBox()
widgets['count'].setRange(1, 5000)
widgets['count'].setValue(300)
layout.addWidget(widgets['count'])
widgets['min_size'] = QtWidgets.QDoubleSpinBox()
widgets['min_size'].setRange(0.0, 200.0)
widgets['min_size'].setDecimals(3)
widgets['min_size'].setValue(2.0)
layout.addWidget(widgets['min_size'])
widgets['max_size'] = QtWidgets.QDoubleSpinBox()
widgets['max_size'].setRange(0.0, 200.0)
widgets['max_size'].setDecimals(3)
widgets['max_size'].setValue(20.0)
layout.addWidget(widgets['max_size'])
widgets['width'] = QtWidgets.QSpinBox()
widgets['width'].setRange(16, 2048)
widgets['width'].setValue(512)
layout.addWidget(widgets['width'])
widgets['height'] = QtWidgets.QSpinBox()
widgets['height'].setRange(16, 2048)
widgets['height'].setValue(512)
layout.addWidget(widgets['height'])
widgets['preview'] = QtWidgets.QLabel()
widgets['preview'].setMinimumSize(160, 160)
from PySide6.QtCore import Qt
widgets['preview'].setAlignment(Qt.AlignmentFlag.AlignCenter)
layout.addWidget(widgets['preview'])
```

### GUI State Handler

```python
def get_values(widgets):
    return {'count': widgets['count'].value(), 'min_size': widgets['min_size'].value(), 'max_size': widgets['max_size'].value(), 'width': widgets['width'].value(), 'height': widgets['height'].value()}

def set_values(widgets, outputs):
    img = outputs.get('image')
    preview = widgets.get('preview')
    if img is not None and preview is not None:
        from PySide6.QtGui import QPixmap
        from PySide6.QtCore import Qt
        pix = QPixmap.fromImage(img)
        preview.setPixmap(pix.scaled(preview.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation))

def set_initial_state(widgets, state):
    if 'count' in state: widgets['count'].setValue(state['count'])
    if 'min_size' in state: widgets['min_size'].setValue(state['min_size'])
    if 'max_size' in state: widgets['max_size'].setValue(state['max_size'])
    if 'width' in state: widgets['width'].setValue(state['width'])
    if 'height' in state: widgets['height'].setValue(state['height'])

```


## Node: Save Image (ID: 03d54455-9560-42d6-945d-1869ddb4f6c7)

### Metadata

```json
{
  "uuid": "03d54455-9560-42d6-945d-1869ddb4f6c7",
  "title": "Save Image",
  "pos": [
    0.0,
    -150.0
  ],
  "size": [
    250,
    167
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "path": "generated/demo.png"
  }
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def save_image(image: QImage = None, path: str = "output.png") -> str:
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

```

### GUI Definition

```python
widgets['path'] = QtWidgets.QLineEdit('output.png')
_row_path = QtWidgets.QHBoxLayout()
_browse_btn_path = QtWidgets.QPushButton('Browse...')
def _browse_pick_path():
    from PySide6.QtWidgets import QFileDialog
    picked, _ = QFileDialog.getSaveFileName(None, 'Save Image', widgets['path'].text(), 'PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)')
    if picked: widgets['path'].setText(picked)
_browse_btn_path.clicked.connect(_browse_pick_path)
_row_path.addWidget(widgets['path'])
_row_path.addWidget(_browse_btn_path)
layout.addLayout(_row_path)
```

### GUI State Handler

```python
def get_values(widgets):
    return {'path': widgets['path'].text()}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    if 'path' in state: widgets['path'].setText(state['path'])

```


## Connections

```json
[
  {
    "start_node_uuid": "15b8a312-abb4-4040-bfbf-2ccf8131a587",
    "start_pin_uuid": "710574eb-2a5e-4ffd-830c-24b7fb490487",
    "start_pin_name": "output_1",
    "end_node_uuid": "ba9f8e1f-0772-4a38-9747-bbdd4934d5ec",
    "end_pin_uuid": "949cddd3-7ee4-4d97-964f-1a97548fb4de",
    "end_pin_name": "child"
  },
  {
    "start_node_uuid": "15b8a312-abb4-4040-bfbf-2ccf8131a587",
    "start_pin_uuid": "20974bb1-b8ce-485c-a6c3-22459d378b4a",
    "start_pin_name": "exec_out",
    "end_node_uuid": "ba9f8e1f-0772-4a38-9747-bbdd4934d5ec",
    "end_pin_uuid": "457d7c40-daf8-4c54-a1b6-08c593f040ef",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "ba9f8e1f-0772-4a38-9747-bbdd4934d5ec",
    "start_pin_uuid": "4200a706-c6c4-4886-96bd-c3e90dd4d649",
    "start_pin_name": "output_1",
    "end_node_uuid": "c1c2fd7b-d76e-483a-9098-2df704862a67",
    "end_pin_uuid": "c3ae009e-64c5-4b23-9c6c-d8f3c701fe14",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "ba9f8e1f-0772-4a38-9747-bbdd4934d5ec",
    "start_pin_uuid": "8cef0fd0-232c-49d1-96da-4c40aa5335b8",
    "start_pin_name": "exec_out",
    "end_node_uuid": "c1c2fd7b-d76e-483a-9098-2df704862a67",
    "end_pin_uuid": "d357f9c1-6ab5-4b6a-b067-2811b1cdb847",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "c1c2fd7b-d76e-483a-9098-2df704862a67",
    "start_pin_uuid": "44b75e90-e0e5-44c1-abc5-cf862606c2a2",
    "start_pin_name": "image",
    "end_node_uuid": "03d54455-9560-42d6-945d-1869ddb4f6c7",
    "end_pin_uuid": "be16bca5-99a3-4f5f-89a0-5a7ecf1692c5",
    "end_pin_name": "image"
  },
  {
    "start_node_uuid": "c1c2fd7b-d76e-483a-9098-2df704862a67",
    "start_pin_uuid": "15c9d10a-e543-4ceb-a5f3-1e1757012c1a",
    "start_pin_name": "exec_out",
    "end_node_uuid": "03d54455-9560-42d6-945d-1869ddb4f6c7",
    "end_pin_uuid": "cfd59bf4-e7b4-4cab-981e-4af97b14cfe0",
    "end_pin_name": "exec_in"
  }
]
```
