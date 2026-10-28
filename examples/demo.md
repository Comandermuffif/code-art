# code-art demo

A generative-art flow ending in an image saved to disk.

## Node: Linear Gradient (ID: f4cedaa3-facd-4f6a-aa5e-a2432efd2a6a)

### Metadata

```json
{
  "uuid": "f4cedaa3-facd-4f6a-aa5e-a2432efd2a6a",
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
@node_entry
def linear_gradient() -> "ColorMode":
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


## Node: Invert (ID: f7e19f90-9f8f-463c-bf61-2ec7fc287e4f)

### Metadata

```json
{
  "uuid": "f7e19f90-9f8f-463c-bf61-2ec7fc287e4f",
  "title": "Invert",
  "pos": [
    -500.0,
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
@node_entry
def invert(child: "ColorMode" = None) -> "ColorMode":
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


## Node: Draw Circles (ID: 7ccbd926-0c1e-4b93-ac30-8583d0e2d63c)

### Metadata

```json
{
  "uuid": "7ccbd926-0c1e-4b93-ac30-8583d0e2d63c",
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
@node_entry
def circles(field: "ColorMode" = None, count: int = 300, min_size: float = 2, max_size: float = 20, width: int = 512, height: int = 512) -> "QImage":
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


## Node: Save Image (ID: 02e2c651-eb72-48d5-a3d5-001cc8d25b37)

### Metadata

```json
{
  "uuid": "02e2c651-eb72-48d5-a3d5-001cc8d25b37",
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
@node_entry
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
    "start_node_uuid": "f4cedaa3-facd-4f6a-aa5e-a2432efd2a6a",
    "start_pin_uuid": "37fa527f-4d9a-4211-92bb-8d36b3039ab8",
    "start_pin_name": "output_1",
    "end_node_uuid": "f7e19f90-9f8f-463c-bf61-2ec7fc287e4f",
    "end_pin_uuid": "ff402c26-fddd-4d71-892f-e5609f045ace",
    "end_pin_name": "child"
  },
  {
    "start_node_uuid": "f4cedaa3-facd-4f6a-aa5e-a2432efd2a6a",
    "start_pin_uuid": "459a998c-ef54-4b63-a30d-6e1b5dab066f",
    "start_pin_name": "exec_out",
    "end_node_uuid": "f7e19f90-9f8f-463c-bf61-2ec7fc287e4f",
    "end_pin_uuid": "35059716-3234-4cf1-97b3-6f0be225eb4e",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "f7e19f90-9f8f-463c-bf61-2ec7fc287e4f",
    "start_pin_uuid": "79bd2780-953e-424d-a53d-a2f563fb36cb",
    "start_pin_name": "output_1",
    "end_node_uuid": "7ccbd926-0c1e-4b93-ac30-8583d0e2d63c",
    "end_pin_uuid": "4dcf79cb-94a7-483d-a7b2-0ebc620e93f9",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "f7e19f90-9f8f-463c-bf61-2ec7fc287e4f",
    "start_pin_uuid": "c710f3bd-48e7-4c02-90b3-86c49a2d4dc3",
    "start_pin_name": "exec_out",
    "end_node_uuid": "7ccbd926-0c1e-4b93-ac30-8583d0e2d63c",
    "end_pin_uuid": "b7ea652d-f606-4383-a2bb-fff475377a0f",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "7ccbd926-0c1e-4b93-ac30-8583d0e2d63c",
    "start_pin_uuid": "9d1270d9-88d8-4afb-ba9a-933cd7689cfb",
    "start_pin_name": "image",
    "end_node_uuid": "02e2c651-eb72-48d5-a3d5-001cc8d25b37",
    "end_pin_uuid": "3aa5ccac-9543-49b8-a6aa-8deb65a8be18",
    "end_pin_name": "image"
  },
  {
    "start_node_uuid": "7ccbd926-0c1e-4b93-ac30-8583d0e2d63c",
    "start_pin_uuid": "e3840d33-1c9d-46bc-8e58-0b65f3a5331e",
    "start_pin_name": "exec_out",
    "end_node_uuid": "02e2c651-eb72-48d5-a3d5-001cc8d25b37",
    "end_pin_uuid": "1a9547a8-0b87-4045-8041-a0d05b43d1d4",
    "end_pin_name": "exec_in"
  }
]
```
