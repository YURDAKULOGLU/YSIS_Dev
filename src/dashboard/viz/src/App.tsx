import { useEffect, useRef, useState } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import { fetchSubgraph, GraphEdge, GraphNode } from "./api";

const DEFAULT_NODE = "ROOT";
const DEFAULT_EDGES = ["imports", "tests", "docs"];

function seedGraph(): { nodes: GraphNode[]; edges: GraphEdge[] } {
  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];
  for (let i = 0; i < 50; i += 1) {
    nodes.push({ id: `N${i}`, label: `Node ${i}`, type: "file" });
    if (i > 0) {
      edges.push({ source: `N${i - 1}`, target: `N${i}`, type: "imports" });
    }
  }
  return { nodes, edges };
}

export default function App() {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const [status, setStatus] = useState("Loading subgraph...");

  useEffect(() => {
    let mounted = true;

    const init = async () => {
      let data: { nodes: GraphNode[]; edges: GraphEdge[] };
      try {
        data = await fetchSubgraph(DEFAULT_NODE, 2, DEFAULT_EDGES);
        if (!mounted) return;
      } catch (err) {
        data = seedGraph();
        if (!mounted) return;
        setStatus("Fallback: local seed graph (API unavailable).");
      }

      const graph = new Graph();
      data.nodes.forEach((node, i) => {
        graph.addNode(node.id, {
          label: node.label ?? node.id,
          size: 6,
          x: i,
          y: i,
          color: "#2f6fed"
        });
      });

      data.edges.forEach((edge, i) => {
        const edgeId = edge.id ?? `E${i}`;
        if (!graph.hasEdge(edgeId)) {
          graph.addEdge(edge.source, edge.target, {
            label: edge.type ?? "edge",
            color: "#9aa4b2"
          });
        }
      });

      if (containerRef.current) {
        sigmaRef.current?.kill();
        sigmaRef.current = new Sigma(graph, containerRef.current, {
          renderEdgeLabels: false,
          enableEdgeEvents: true
        });
        setStatus("Subgraph loaded.");
      }
    };

    init();

    return () => {
      mounted = false;
      sigmaRef.current?.kill();
    };
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div className="title">PROJECT NEO - Visualization</div>
        <div className="status">{status}</div>
      </header>
      <div className="graph-container" ref={containerRef} />
    </div>
  );
}
