st.write\_stream - Streamlit Docs

## st.write\_stream

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Stream a generator, iterable, or stream-like sequence to the app.

st.write\_stream iterates through the given sequences and writes all
chunks to the app. String chunks will be written using a typewriter effect.
Other data types will be written using st.write.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/write.py#L64 "View st.write_stream source code on GitHub") | |
| --- | --- |
| st.write\_stream(stream, \*, cursor=None) | |
| Parameters | |
| stream (Callable, Generator, Iterable, OpenAI Stream, or LangChain Stream) | The generator or iterable to stream.  If you pass an async generator, Streamlit will internally convert it to a sync generator. If the generator depends on a cached object with async references, this can raise an error.  Note  To use additional LLM libraries, you can create a wrapper to manually define a generator function and include custom output parsing. |
| cursor (str or None) | A string to append to text as it's being written. If this is None (default), no cursor is shown. Otherwise, the string is rendered as Markdown and appears as a cursor at the end of the streamed text. For example, you can use an emoji, emoji shortcode, or Material icon.  The first line of the cursor string can contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height. If you pass a multiline string, additional lines display after the text with the full Markdown rendering capabilities of st.markdown.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
|  |  |
| --- | --- |
| Returns | |
| (str or list) | The full response. If the streamed output only contains text, this is a string. Otherwise, this is a list of all the streamed objects. The return value is fully compatible as input for st.write. |

#### Example

You can pass an OpenAI stream as shown in our tutorial, [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/llms /build-conversational-apps#build-a-chatgpt-like-app). Alternatively,
you can pass a generic generator function as input:

```
import time
import numpy as np
import pandas as pd
import streamlit as st

_LOREM_IPSUM = \"\"\"
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
\"\"\"


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-write-stream-data.streamlit.app//?utm_medium=oembed&)

*star*

#### Tip

If your stream object is not compatible with `st.write_stream`, define a wrapper around your stream object to create a compatible generator function.

`for chunk in unsupported_stream:
yield preprocess(chunk)`

For an example, see how we use [Replicate](https://replicate.com/docs/get-started/python) with [Snowflake Arctic](https://www.snowflake.com/en/data-cloud/arctic/) in [this code](https://github.com/streamlit/snowflake-arctic-st-demo/blob/0f0d8b49f328f72ae58ced2e9000790fb5e56e6f/simple_app.py#L58).

[*arrow\_back*Previous: st.write](/develop/api-reference/write-magic/st.write)[*arrow\_forward*Next: magic](/develop/api-reference/write-magic/magic)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI