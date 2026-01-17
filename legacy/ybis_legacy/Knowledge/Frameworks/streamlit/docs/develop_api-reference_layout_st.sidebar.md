st.sidebar - Streamlit Docs

## st.sidebar

## Add widgets to sidebar

Not only can you add interactivity to your app with widgets, you can organize them into a sidebar. Elements can be passed to `st.sidebar` using object notation and `with` notation.

The following two snippets are equivalent:

`# Object notation
st.sidebar.[element_name]`

`# "with" notation
with st.sidebar:
st.[element_name]`

Each element that's passed to `st.sidebar` is pinned to the left, allowing users to focus on the content in your app.

*star*

#### Tip

The sidebar is resizable! Drag and drop the right border of the sidebar to resize it! ↔️

Here's an example of how you'd add a selectbox and a radio button to your sidebar:

`import streamlit as st
# Using object notation
add_selectbox = st.sidebar.selectbox(
"How would you like to be contacted?",
("Email", "Home phone", "Mobile phone")
)
# Using "with" notation
with st.sidebar:
add_radio = st.radio(
"Choose a shipping method",
("Standard (5-15 days)", "Express (2-5 days)")
)`

*priority\_high*

#### Important

The only elements that aren't supported using object notation are `st.echo`, `st.spinner`, and `st.toast`. To use these elements, you must use `with` notation.

Here's an example of how you'd add [`st.echo`](/develop/api-reference/text/st.echo) and [`st.spinner`](/develop/api-reference/status/st.spinner) to your sidebar:

`import streamlit as st
import time
with st.sidebar:
with st.echo():
st.write("This code will be printed to the sidebar.")
with st.spinner("Loading..."):
time.sleep(5)
st.success("Done!")`

[*arrow\_back*Previous: st.popover](/develop/api-reference/layout/st.popover)[*arrow\_forward*Next: st.space](/develop/api-reference/layout/st.space)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI