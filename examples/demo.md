# code-art demo

Two generative-art chains built with code-art nodes.

## Node: Linear Gradient (ID: 574f8021-dfce-4bf2-9cda-48416981868d)

### Metadata

```json
{
  "uuid": "574f8021-dfce-4bf2-9cda-48416981868d",
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
    from color_modes.linear_gradient import LinearGradientColorMode
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


## Node: Invert (ID: ac510033-0a2f-4666-af40-e9ba312ed1a0)

### Metadata

```json
{
  "uuid": "ac510033-0a2f-4666-af40-e9ba312ed1a0",
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
    from color_modes.modify.invert import InvertColorMode
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


## Node: Draw Circles (ID: 9326ffe4-262d-457a-b578-2bd742049d97)

### Metadata

```json
{
  "uuid": "9326ffe4-262d-457a-b578-2bd742049d97",
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
    from render import render_to_qimage
    from render.circles import draw_circles
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


## Node: Grid (ID: 153c241e-432c-4c24-8e87-a92e9d81e756)

### Metadata

```json
{
  "uuid": "153c241e-432c-4c24-8e87-a92e9d81e756",
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
    from color_modes.grid import GridColorMode
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


## Node: Draw Hexagon (ID: bd094400-ebd8-4f59-a737-818f437a267d)

### Metadata

```json
{
  "uuid": "bd094400-ebd8-4f59-a737-818f437a267d",
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
    from render import render_to_qimage
    from render.hexagon import draw_hexagon
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
    "start_node_uuid": "574f8021-dfce-4bf2-9cda-48416981868d",
    "start_pin_uuid": "13a1c034-a6ae-4c01-b452-ca4369c85f17",
    "start_pin_name": "output_1",
    "end_node_uuid": "ac510033-0a2f-4666-af40-e9ba312ed1a0",
    "end_pin_uuid": "b5975314-7e1e-42f6-8b72-ef4714a151a9",
    "end_pin_name": "child"
  },
  {
    "start_node_uuid": "574f8021-dfce-4bf2-9cda-48416981868d",
    "start_pin_uuid": "7221abf2-f0eb-4519-9557-563e8f1588dd",
    "start_pin_name": "exec_out",
    "end_node_uuid": "ac510033-0a2f-4666-af40-e9ba312ed1a0",
    "end_pin_uuid": "8ca27dff-0636-4bf6-812a-b9037fa5fb24",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "ac510033-0a2f-4666-af40-e9ba312ed1a0",
    "start_pin_uuid": "31edef48-673a-498d-9471-669f0b2ca8a6",
    "start_pin_name": "output_1",
    "end_node_uuid": "9326ffe4-262d-457a-b578-2bd742049d97",
    "end_pin_uuid": "04ec4354-a22c-4545-b810-327dbb0a01c5",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "ac510033-0a2f-4666-af40-e9ba312ed1a0",
    "start_pin_uuid": "be86bd94-441e-4954-a7f8-6b4b5f0aa806",
    "start_pin_name": "exec_out",
    "end_node_uuid": "9326ffe4-262d-457a-b578-2bd742049d97",
    "end_pin_uuid": "3278b3df-7ffa-48f4-a690-59d5a703a2dc",
    "end_pin_name": "exec_in"
  },
  {
    "start_node_uuid": "153c241e-432c-4c24-8e87-a92e9d81e756",
    "start_pin_uuid": "45506344-a5ad-484a-a692-a03b353d5aad",
    "start_pin_name": "output_1",
    "end_node_uuid": "bd094400-ebd8-4f59-a737-818f437a267d",
    "end_pin_uuid": "fb8634d0-93f1-419a-a5f4-1fc8cda5a252",
    "end_pin_name": "field"
  },
  {
    "start_node_uuid": "153c241e-432c-4c24-8e87-a92e9d81e756",
    "start_pin_uuid": "9061e40d-ddaf-40dd-a162-bfcefe6b6a8f",
    "start_pin_name": "exec_out",
    "end_node_uuid": "bd094400-ebd8-4f59-a737-818f437a267d",
    "end_pin_uuid": "faccd726-2adf-48f3-a76e-902182228f25",
    "end_pin_name": "exec_in"
  }
]
```
