# code-art demo

Two generative-art chains built with code-art nodes.

## Node: Linear Gradient (ID: 4385a5ee-2166-4891-8cb8-2bd5443384af)

### Metadata

```json
{
  "uuid": "4385a5ee-2166-4891-8cb8-2bd5443384af",
  "title": "Linear Gradient",
  "pos": [
    -600.0,
    -300.0
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


## Node: Invert (ID: 294331e4-8b21-4b25-8c40-45817b74ecbf)

### Metadata

```json
{
  "uuid": "294331e4-8b21-4b25-8c40-45817b74ecbf",
  "title": "Invert",
  "pos": [
    -350.0,
    -300.0
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


## Node: Draw Circles (ID: 6e16c7ac-9aef-4558-bc43-d14d2babcc26)

### Metadata

```json
{
  "uuid": "6e16c7ac-9aef-4558-bc43-d14d2babcc26",
  "title": "Draw Circles",
  "pos": [
    -80.0,
    -300.0
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


## Node: Grid (ID: 713915fd-a6ec-4672-aab0-3983acffdddb)

### Metadata

```json
{
  "uuid": "713915fd-a6ec-4672-aab0-3983acffdddb",
  "title": "Grid",
  "pos": [
    -600.0,
    200.0
  ],
  "size": [
    250,
    150
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "colors": "#ff0000,#00ff00,#0000ff,#ffff00"
  }
}
```

### Logic

```python
@node_entry
def grid(colors: str = "#ff0000,#00ff00,#0000ff,#ffff00") -> "ColorMode":
    from models import FloatColor
    from nodes.color.grid import GridColorMode
    return GridColorMode(FloatColor.fromHexList(colors))

```

### GUI Definition

```python
widgets['colors'] = QtWidgets.QLineEdit('#ff0000,#00ff00,#0000ff,#ffff00')
layout.addWidget(widgets['colors'])
```

### GUI State Handler

```python
def get_values(widgets):
    return {'colors': widgets['colors'].text()}

def set_values(widgets, outputs):
    pass

def set_initial_state(widgets, state):
    if 'colors' in state: widgets['colors'].setText(state['colors'])

```


## Node: Draw Hexagon (ID: 1fb3b8ca-f6f0-468a-b5ac-ca3cf31f3a9f)

### Metadata

```json
{
  "uuid": "1fb3b8ca-f6f0-468a-b5ac-ca3cf31f3a9f",
  "title": "Draw Hexagon",
  "pos": [
    -350.0,
    200.0
  ],
  "size": [
    250,
    242
  ],
  "colors": {
    "title": "#2a2a2a",
    "body": "#141414"
  },
  "gui_state": {
    "count": 12,
    "radious": 0.8,
    "width": 512,
    "height": 512
  }
}
```

### Logic

```python
@node_entry
def hexagon(field: "ColorMode" = None, count: int = 12, radious: float = 0.8, width: int = 512, height: int = 512) -> "QImage":
    """@outputs: image"""
    from nodes.draw._render import render_to_qimage
    from nodes.draw.hexagon import draw_hexagon
    return render_to_qimage(field, draw_hexagon, width, height, count=count, radious=radious)

```

### GUI Definition

```python
widgets['count'] = QtWidgets.QSpinBox()
widgets['count'].setRange(1, 100)
widgets['count'].setValue(12)
layout.addWidget(widgets['count'])
widgets['radious'] = QtWidgets.QDoubleSpinBox()
widgets['radious'].setRange(0.0, 2.0)
widgets['radious'].setDecimals(3)
widgets['radious'].setValue(0.8)
layout.addWidget(widgets['radious'])
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
    return {'count': widgets['count'].value(), 'radious': widgets['radious'].value(), 'width': widgets['width'].value(), 'height': widgets['height'].value()}

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
    if 'radious' in state: widgets['radious'].setValue(state['radious'])
    if 'width' in state: widgets['width'].setValue(state['width'])
    if 'height' in state: widgets['height'].setValue(state['height'])

```


## Connections

```json
[
  {
    "start_node_uuid": "4385a5ee-2166-4891-8cb8-2bd5443384af",
    "start_pin_uuid": "619ed263-e54b-43b9-aab1-bdd5eba50186",
    "start_pin_name": "output_1",
    "end_node_uuid": "294331e4-8b21-4b25-8c40-45817b74ecbf",
    "end_pin_uuid": "877f1d63-8138-4b60-bc16-ff6a175fdd9f",
    "end_pin_name": "child"
  },
  {
    "start_node_uuid": "4385a5ee-2166-4891-8cb8-2bd5443384af",
    "start_pin_uuid": "7f57f489-ebe1-4933-a5ab-70a7bf502648",
    "start_pin_name": "exec_out",
    "end_node_uuid": "294331e4-8b21-4b25-8c40-45817b74ecbf",
    "end_pin_uuid": "32e8bab5-29bd-48e3-b653-9dfb808b9a2f",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "294331e4-8b21-4b25-8c40-45817b74ecbf",
    "start_pin_uuid": "549fa32d-2159-4e74-9058-d9bbe7151458",
    "start_pin_name": "output_1",
    "end_node_uuid": "6e16c7ac-9aef-4558-bc43-d14d2babcc26",
    "end_pin_uuid": "b2219b9d-d1f5-419f-aa49-18b5ea2b2cd4",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "294331e4-8b21-4b25-8c40-45817b74ecbf",
    "start_pin_uuid": "b6d181b6-f55f-49f5-bb47-5d78eb90c464",
    "start_pin_name": "exec_out",
    "end_node_uuid": "6e16c7ac-9aef-4558-bc43-d14d2babcc26",
    "end_pin_uuid": "6b4e20f4-e2e2-4083-b193-90b50c8c0bf7",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "713915fd-a6ec-4672-aab0-3983acffdddb",
    "start_pin_uuid": "f331653d-3f0a-41fb-868b-0aa56cf1da8d",
    "start_pin_name": "output_1",
    "end_node_uuid": "1fb3b8ca-f6f0-468a-b5ac-ca3cf31f3a9f",
    "end_pin_uuid": "cb5f68ee-6546-439c-8b6d-ac016aafabcd",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "713915fd-a6ec-4672-aab0-3983acffdddb",
    "start_pin_uuid": "85f05e6e-eada-4ba0-9442-a75413258e73",
    "start_pin_name": "exec_out",
    "end_node_uuid": "1fb3b8ca-f6f0-468a-b5ac-ca3cf31f3a9f",
    "end_pin_uuid": "0e44d9b1-38d9-4545-8afd-e9d6aa466079",
    "end_pin_name": "exec_in"
  }
]
```
