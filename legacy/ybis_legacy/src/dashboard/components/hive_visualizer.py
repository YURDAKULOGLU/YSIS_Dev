
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from src.agentic.infrastructure.graph_db import GraphDB

def fetch_hive_data():
    """Fetch Agents, Tasks, and Relationships from Neo4j"""
    nodes = []
    edges = []

    query = """
    MATCH (n)
    WHERE labels(n)[0] IN ['Agent', 'Task', 'CodeFile', 'Function']
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m LIMIT 100
    """

    with GraphDB() as db:
        results = db.driver.execute_query(query)

        seen_nodes = set()

        for record in results.records:
            n = record['n']
            r = record['r']
            m = record['m']

            # Process Source Node
            n_id = n.get('id') or n.get('path') or n.get('qualified_name') or str(n.element_id)
            if n_id not in seen_nodes:
                label = list(n.labels)[0]
                color = "#FF4B4B" if label == "Task" else "#1C83E1" if label == "Agent" else "#00C496"
                nodes.append(Node(id=n_id, label=n.get('name') or n_id.split('/')[-1], size=25, color=color))
                seen_nodes.add(n_id)

            # Process Target Node and Edge
            if m:
                m_id = m.get('id') or m.get('path') or m.get('qualified_name') or str(m.element_id)
                if m_id not in seen_nodes:
                    label = list(m.labels)[0]
                    color = "#FF4B4B" if label == "Task" else "#1C83E1" if label == "Agent" else "#00C496"
                    nodes.append(Node(id=m_id, label=m.get('name') or m_id.split('/')[-1], size=25, color=color))
                    seen_nodes.add(m_id)

                edges.append(Edge(source=n_id, target=m_id, label=r.type))

    return nodes, edges

def render_hive_mind():
    st.subheader("[INFO] The Hive Mind Graph")
    st.caption("Red: Tasks | Blue: Agents | Green: Code/Docs")

    nodes, edges = fetch_hive_data()

    config = Config(width=900,
                    height=600,
                    directed=True,
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6",
                    collapsible=False,
                    node={'labelProperty': 'label'},
                    link={'labelProperty': 'label', 'renderLabel': True}
                    )

    return agraph(nodes=nodes, edges=edges, config=config)
