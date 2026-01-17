st.echo - Streamlit Docs

## st.echo

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Use in a with block to draw some code on the app, then execute it.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/commands/echo.py#L33 "View st.echo source code on GitHub") | |
| --- | --- |
| st.echo(code\_location="above") | |
| Parameters | |
| code\_location ("above" or "below") | Whether to show the echoed code before or after the results of the executed code block. |

#### Example

```
import streamlit as st

with st.echo():
    st.write('This code will be printed')
```

### Display code

Sometimes you want your Streamlit app to contain *both* your usual
Streamlit graphic elements *and* the code that generated those elements.
That's where `st.echo()` comes in.

Ok so let's say you have the following file, and you want to make its
app a little bit more self-explanatory by making that middle section
visible in the Streamlit app:

`import streamlit as st
def get_user_name():
return 'John'
# ------------------------------------------------
# Want people to see this part of the code...
def get_punctuation():
return '!!!'
greeting = "Hi there, "
user_name = get_user_name()
punctuation = get_punctuation()
st.write(greeting, user_name, punctuation)
# ...up to here
# ------------------------------------------------
foo = 'bar'
st.write('Done!')`

The file above creates a Streamlit app containing the words "Hi there,
`John`", and then "Done!".

Now let's use `st.echo()` to make that middle section of the code visible
in the app:

`import streamlit as st
def get_user_name():
return 'John'
with st.echo():
# Everything inside this block will be both printed to the screen
# and executed.
def get_punctuation():
return '!!!'
greeting = "Hi there, "
value = get_user_name()
punctuation = get_punctuation()
st.write(greeting, value, punctuation)
# And now we're back to _not_ printing to the screen
foo = 'bar'
st.write('Done!')`

It's *that* simple!

*push\_pin*

#### Note

You can have multiple `st.echo()` blocks in the same file.
Use it as often as you wish!

[*arrow\_back*Previous: st.divider](/develop/api-reference/text/st.divider)[*arrow\_forward*Next: st.latex](/develop/api-reference/text/st.latex)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI