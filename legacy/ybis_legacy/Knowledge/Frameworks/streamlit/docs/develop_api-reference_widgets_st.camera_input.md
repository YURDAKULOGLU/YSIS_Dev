st.camera\_input - Streamlit Docs

## st.camera\_input

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a widget that returns pictures from the user's webcam.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/camera_input.py#L86 "View st.camera_input source code on GitHub") | |
| --- | --- |
| st.camera\_input(label, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, disabled=False, label\_visibility="visible", width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this widget is used for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this camera\_input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the camera input if set to True. Default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("stretch" or int) | The width of the camera input widget. This can be one of the following:   * "stretch" (default): The width of the widget matches the   width of the parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (None or UploadedFile) | The UploadedFile class is a subclass of BytesIO, and therefore is "file-like". This means you can pass an instance of it anywhere a file is expected. |

#### Examples

```
import streamlit as st

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-camera-input.streamlit.app//?utm_medium=oembed&)

To read the image file buffer as bytes, you can use `getvalue()` on the `UploadedFile` object.

`import streamlit as st
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
# To read image file buffer as bytes:
bytes_data = img_file_buffer.getvalue()
# Check the type of bytes_data:
# Should output: <class 'bytes'>
st.write(type(bytes_data))`

*priority\_high*

#### Important

`st.camera_input` returns an object of the `UploadedFile` class, which a subclass of BytesIO. Therefore it is a "file-like" object. This means you can pass it anywhere where a file is expected, similar to `st.file_uploader`.

## Image processing examples

You can use the output of `st.camera_input` for various downstream tasks, including image processing. Below, we demonstrate how to use the `st.camera_input` widget with popular image and data processing libraries such as [Pillow](https://pillow.readthedocs.io/en/stable/installation.html), [NumPy](https://numpy.org/), [OpenCV](https://pypi.org/project/opencv-python-headless/), [TensorFlow](https://www.tensorflow.org/), [torchvision](https://pytorch.org/vision/stable/index.html), and [PyTorch](https://pytorch.org/).

While we provide examples for the most popular use-cases and libraries, you are welcome to adapt these examples to your own needs and favorite libraries.

### Pillow (PIL) and NumPy

Ensure you have installed [Pillow](https://pillow.readthedocs.io/en/stable/installation.html) and [NumPy](https://numpy.org/).

To read the image file buffer as a PIL Image and convert it to a NumPy array:

`import streamlit as st
from PIL import Image
import numpy as np
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
# To read image file buffer as a PIL Image:
img = Image.open(img_file_buffer)
# To convert PIL Image to numpy array:
img_array = np.array(img)
# Check the type of img_array:
# Should output: <class 'numpy.ndarray'>
st.write(type(img_array))
# Check the shape of img_array:
# Should output shape: (height, width, channels)
st.write(img_array.shape)`

### OpenCV (cv2)

Ensure you have installed [OpenCV](https://pypi.org/project/opencv-python-headless/) and [NumPy](https://numpy.org/).

To read the image file buffer with OpenCV:

`import streamlit as st
import cv2
import numpy as np
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
# To read image file buffer with OpenCV:
bytes_data = img_file_buffer.getvalue()
cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
# Check the type of cv2_img:
# Should output: <class 'numpy.ndarray'>
st.write(type(cv2_img))
# Check the shape of cv2_img:
# Should output shape: (height, width, channels)
st.write(cv2_img.shape)`

### TensorFlow

Ensure you have installed [TensorFlow](https://www.tensorflow.org/install/).

To read the image file buffer as a 3 dimensional uint8 tensor with TensorFlow:

`import streamlit as st
import tensorflow as tf
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
# To read image file buffer as a 3D uint8 tensor with TensorFlow:
bytes_data = img_file_buffer.getvalue()
img_tensor = tf.io.decode_image(bytes_data, channels=3)
# Check the type of img_tensor:
# Should output: <class 'tensorflow.python.framework.ops.EagerTensor'>
st.write(type(img_tensor))
# Check the shape of img_tensor:
# Should output shape: (height, width, channels)
st.write(img_tensor.shape)`

### Torchvision

Ensure you have installed [Torchvision](https://pypi.org/project/torchvision/) (it is not bundled with PyTorch) and [PyTorch](https://pytorch.org/).

To read the image file buffer as a 3 dimensional uint8 tensor with `torchvision.io`:

`` import streamlit as st
import torch
import torchvision
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
# To read image file buffer as a 3D uint8 tensor with `torchvision.io`:
bytes_data = img_file_buffer.getvalue()
torch_img = torchvision.io.decode_image(
torch.frombuffer(bytes_data, dtype=torch.uint8)
)
# Check the type of torch_img:
# Should output: <class 'torch.Tensor'>
st.write(type(torch_img))
# Check the shape of torch_img:
# Should output shape: torch.Size([channels, height, width])
st.write(torch_img.shape) ``

### PyTorch

Ensure you have installed [PyTorch](https://pytorch.org/) and [NumPy](https://numpy.org/).

To read the image file buffer as a 3 dimensional uint8 tensor with PyTorch:

`import streamlit as st
import torch
import numpy as np
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:
# To read image file buffer as a 3D uint8 tensor with PyTorch:
bytes_data = img_file_buffer.getvalue()
torch_img = torch.ops.image.decode_image(
torch.from_numpy(np.frombuffer(bytes_data, np.uint8)), 3
)
# Check the type of torch_img:
# Should output: <class 'torch.Tensor'>
st.write(type(torch_img))
# Check the shape of torch_img:
# Should output shape: torch.Size([channels, height, width])
st.write(torch_img.shape)`

[*arrow\_back*Previous: st.audio\_input](/develop/api-reference/widgets/st.audio_input)[*arrow\_forward*Next: st.data\_editor](https://docs.streamlit.io/develop/api-reference/data/st.data_editor)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI