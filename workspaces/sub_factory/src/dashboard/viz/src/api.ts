export type GraphNode = {
  id: string;
  label?: string;
  type?: string;
  group?: string;
};

export type GraphEdge = {
  id?: string;
  source: string;
  target: string;
  type?: string;
};

export type SubgraphResponse = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export async function fetchSubgraph(
  nodeId: string,
  depth: number,
  edgeTypes: string[]
): Promise<SubgraphResponse> {
  const params = new URLSearchParams({
    id: nodeId,
    depth: String(depth),
    edges: edgeTypes.join(",")
  });

  const res = await fetch(`/api/graph/subgraph?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch subgraph: ${res.status}`);
  }
  return res.json() as Promise<SubgraphResponse>;
}
