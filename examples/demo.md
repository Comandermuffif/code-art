# code-art demo

A generative-art flow ending in an image saved to disk.

## Node: Palette (ID: c33b6287-987f-421b-a7f8-c2f8fed95ae6)

### Metadata

```json
{
  "uuid": "c33b6287-987f-421b-a7f8-c2f8fed95ae6",
  "title": "Palette",
  "pos": [
    -1000.0,
    -150.0
  ],
  "size": [
    272.453125,
    150
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "hex_colors": "#ff0000,#00ff00,#0000ff,#ff0000"
  }
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def palette(hex_colors: str = "#ff0000,#00ff00,#0000ff,#ff0000") -> list[FloatColor]:
    """@outputs: colors"""
    from models import FloatColor
    return FloatColor.fromHexList(hex_colors)

```

### GUI Definition

```python
widgets['hex_colors'] = QtWidgets.QLineEdit('#ff0000,#00ff00,#0000ff,#ff0000')
layout.addWidget(widgets['hex_colors'])
```

### GUI State Handler

```python
def get_values(widgets):
    return {'hex_colors': widgets['hex_colors'].text()}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    if 'hex_colors' in state: widgets['hex_colors'].setText(state['hex_colors'])

```


## Node: Get Subcolors (ID: 2a2c5c63-7ff8-45ff-81b3-9e2091ac59a8)

### Metadata

```json
{
  "uuid": "2a2c5c63-7ff8-45ff-81b3-9e2091ac59a8",
  "title": "Get Subcolors",
  "pos": [
    -750.0,
    -150.0
  ],
  "size": [
    307.0625,
    192
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "subcount": 4,
    "wrap": false
  }
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def subcolors(colors: list[FloatColor] = None, subcount: int = 4, wrap: bool = False) -> list[FloatColor]:
    """@outputs: colors"""
    from models import FloatColor
    if colors is None:
        raise ValueError("Get Subcolors: no color palette connected")
    return FloatColor.getSubcolors(colors, subcount, wrap)

```

### GUI Definition

```python
widgets['subcount'] = QtWidgets.QSpinBox()
widgets['subcount'].setRange(0, 64)
widgets['subcount'].setValue(4)
layout.addWidget(widgets['subcount'])
widgets['wrap'] = QtWidgets.QCheckBox('wrap')
widgets['wrap'].setChecked(False)
layout.addWidget(widgets['wrap'])
```

### GUI State Handler

```python
def get_values(widgets):
    return {'subcount': widgets['subcount'].value(), 'wrap': widgets['wrap'].isChecked()}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    if 'subcount' in state: widgets['subcount'].setValue(state['subcount'])
    if 'wrap' in state: widgets['wrap'].setChecked(bool(state['wrap']))

```


## Node: Gradient (ID: eaa06a39-f015-4864-9c0c-27c24922be6c)

### Metadata

```json
{
  "uuid": "eaa06a39-f015-4864-9c0c-27c24922be6c",
  "title": "Gradient",
  "pos": [
    -500.0,
    -150.0
  ],
  "size": [
    304.234375,
    167
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "orientation": 0
  }
}
```

### Logic

```python
from __future__ import annotations

@node_entry
def gradient(colors: list[FloatColor] = None, orientation: int = 0) -> ColorMode:
    from nodes.color.gradient import GradientColorMode
    if colors is None:
        raise ValueError("Gradient: no color palette connected")
    return GradientColorMode(colors, orientation)

```

### GUI Definition

```python
widgets['orientation'] = QtWidgets.QSpinBox()
widgets['orientation'].setRange(0, 2)
widgets['orientation'].setValue(0)
layout.addWidget(widgets['orientation'])
```

### GUI State Handler

```python
def get_values(widgets):
    return {'orientation': widgets['orientation'].value()}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    if 'orientation' in state: widgets['orientation'].setValue(state['orientation'])

```


## Node: Invert (ID: 88821422-8c3a-4ad3-bacb-ad2850eb9e5e)

### Metadata

```json
{
  "uuid": "88821422-8c3a-4ad3-bacb-ad2850eb9e5e",
  "title": "Invert",
  "pos": [
    -250.0,
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


## Node: Draw Circles (ID: 9c394a7a-da35-4ce3-883b-e0af1c27cca3)

### Metadata

```json
{
  "uuid": "9c394a7a-da35-4ce3-883b-e0af1c27cca3",
  "title": "Draw Circles",
  "pos": [
    0.0,
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


## Node: Save Image (ID: d8c0c2c8-38dc-47b9-b84b-150b9e35765a)

### Metadata

```json
{
  "uuid": "d8c0c2c8-38dc-47b9-b84b-150b9e35765a",
  "title": "Save Image",
  "pos": [
    250.0,
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
    "start_node_uuid": "c33b6287-987f-421b-a7f8-c2f8fed95ae6",
    "start_pin_uuid": "bf2def4c-cd7a-4c54-8ae5-a474c122a461",
    "start_pin_name": "colors",
    "end_node_uuid": "2a2c5c63-7ff8-45ff-81b3-9e2091ac59a8",
    "end_pin_uuid": "65462b79-e9ca-4a8a-9ea8-c7f8f41d6557",
    "end_pin_name": "colors"
  },
  {
    "start_node_uuid": "c33b6287-987f-421b-a7f8-c2f8fed95ae6",
    "start_pin_uuid": "03cd4ebf-d16a-40af-85c9-2e27a491562d",
    "start_pin_name": "exec_out",
    "end_node_uuid": "2a2c5c63-7ff8-45ff-81b3-9e2091ac59a8",
    "end_pin_uuid": "5cda24bb-ef71-42f5-b427-f89936dc24a3",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "2a2c5c63-7ff8-45ff-81b3-9e2091ac59a8",
    "start_pin_uuid": "a3d9290c-2c81-49a8-9e82-0da64f4b5e5e",
    "start_pin_name": "colors",
    "end_node_uuid": "eaa06a39-f015-4864-9c0c-27c24922be6c",
    "end_pin_uuid": "63d1c54f-13da-43ae-93a5-6baee025b911",
    "end_pin_name": "colors"
  },
  {
    "start_node_uuid": "2a2c5c63-7ff8-45ff-81b3-9e2091ac59a8",
    "start_pin_uuid": "e7153f5c-e5a5-4ee4-a7c9-98f27582c681",
    "start_pin_name": "exec_out",
    "end_node_uuid": "eaa06a39-f015-4864-9c0c-27c24922be6c",
    "end_pin_uuid": "be98b66e-b4a7-47b7-adb2-28542b757f60",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "eaa06a39-f015-4864-9c0c-27c24922be6c",
    "start_pin_uuid": "1d5158e1-08a1-4056-a915-c5696522f997",
    "start_pin_name": "output_1",
    "end_node_uuid": "88821422-8c3a-4ad3-bacb-ad2850eb9e5e",
    "end_pin_uuid": "58375c9e-e258-415c-bd7b-47aecca7f1e1",
    "end_pin_name": "child"
  },
  {
    "start_node_uuid": "eaa06a39-f015-4864-9c0c-27c24922be6c",
    "start_pin_uuid": "d5e4f2df-77e4-4ba9-8b3a-a6f999d4d8e9",
    "start_pin_name": "exec_out",
    "end_node_uuid": "88821422-8c3a-4ad3-bacb-ad2850eb9e5e",
    "end_pin_uuid": "72985a0f-cebc-46c1-809e-565df3ac6a66",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "88821422-8c3a-4ad3-bacb-ad2850eb9e5e",
    "start_pin_uuid": "3d0e28ef-b185-4cbd-9deb-e1f879c6fdcc",
    "start_pin_name": "output_1",
    "end_node_uuid": "9c394a7a-da35-4ce3-883b-e0af1c27cca3",
    "end_pin_uuid": "5b36d665-d5d9-4815-9610-9ae332786a79",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "88821422-8c3a-4ad3-bacb-ad2850eb9e5e",
    "start_pin_uuid": "2644a012-812c-4441-bfd1-a956ffd1a1fe",
    "start_pin_name": "exec_out",
    "end_node_uuid": "9c394a7a-da35-4ce3-883b-e0af1c27cca3",
    "end_pin_uuid": "e9d47956-623c-4e82-a379-47f630ed3bf3",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "9c394a7a-da35-4ce3-883b-e0af1c27cca3",
    "start_pin_uuid": "bad87cdf-5fff-4374-bad1-00349cd844ca",
    "start_pin_name": "image",
    "end_node_uuid": "d8c0c2c8-38dc-47b9-b84b-150b9e35765a",
    "end_pin_uuid": "3deb34fc-7cfe-488c-a302-78104d7dd4e6",
    "end_pin_name": "image"
  },
  {
    "start_node_uuid": "9c394a7a-da35-4ce3-883b-e0af1c27cca3",
    "start_pin_uuid": "27422407-9c1d-4faa-af36-f6114600ddcd",
    "start_pin_name": "exec_out",
    "end_node_uuid": "d8c0c2c8-38dc-47b9-b84b-150b9e35765a",
    "end_pin_uuid": "f6087077-95e7-42d4-b3b2-3b295fefc15c",
    "end_pin_name": "exec_in"
  }
]
```
