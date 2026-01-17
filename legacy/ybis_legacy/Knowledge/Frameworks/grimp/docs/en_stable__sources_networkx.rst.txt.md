========
NetworkX
========
If you want to analyze the graph in a way that isn't provided by Grimp, you may want to consider converting the graph to a `NetworkX`\_ graph.
NetworkX is a third-party Python library with a large number of algorithms for working with graphs.
Converting the Grimp graph to a NetworkX graph
----------------------------------------------
First, you should install NetworkX (e.g. ``pip install networkx``).
You can then build up a NetworkX graph as shown::
import grimp
import networkx
grimp\_graph = grimp.build\_graph("mypackage")
# Build a NetworkX graph from the Grimp graph.
networkx\_graph = networkx.DiGraph()
for module in grimp\_graph.modules:
networkx\_graph.add\_node(module)
for imported in grimp\_graph.find\_modules\_directly\_imported\_by(module):
networkx\_graph.add\_edge(module, imported)
.. \_NetworkX: https://networkx.org/