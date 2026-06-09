(async function () {
  const response = await fetch("/api/graph");
  const graph = await response.json();
  if (graph.error) {
    renderError(graph.error);
    return;
  }

  const clusterSelect = document.getElementById("clusterSelect");
  for (const cluster of graph.clusters) {
    const option = document.createElement("option");
    option.value = cluster.id;
    option.textContent = cluster.name;
    clusterSelect.appendChild(option);
  }

  const kindColors = {
    dataset: "#2f7d6d",
    process: "#7a4f9f",
    spec: "#c05a36",
    document: "#496cba",
    code: "#5d7480",
  };

  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [
      ...graph.nodes.map((node) => ({
        data: {
          id: node.id,
          label: node.label,
          kind: node.kind,
          props: node.props,
        },
      })),
      ...graph.relations.map((relation) => ({
        data: {
          id: relation.id,
          source: relation.src,
          target: relation.dst,
          label: relation.type,
          props: relation.props,
        },
      })),
    ],
    style: [
      {
        selector: "node",
        style: {
          "background-color": (element) =>
            kindColors[element.data("kind")] || "#6f767d",
          label: "data(label)",
          color: "#202124",
          "font-size": 12,
          "text-valign": "bottom",
          "text-halign": "center",
          "text-margin-y": 8,
          "border-width": 2,
          "border-color": "#ffffff",
          width: 34,
          height: 34,
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": "#9aa0a6",
          "target-arrow-color": "#9aa0a6",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
          label: "data(label)",
          color: "#4f5357",
          "font-size": 11,
          "text-background-color": "#ffffff",
          "text-background-opacity": 0.9,
          "text-background-padding": 2,
        },
      },
      {
        selector: ".faded",
        style: {
          opacity: 0.18,
        },
      },
      {
        selector: "edge.clusterEdge",
        style: {
          width: 5,
          "line-color": "#d45f3a",
          "target-arrow-color": "#d45f3a",
          opacity: 1,
          "z-index": 10,
        },
      },
      {
        selector: "node.clusterNode",
        style: {
          "border-width": 4,
          "border-color": "#d45f3a",
          opacity: 1,
        },
      },
    ],
    layout: {
      name: "cose",
      animate: true,
      fit: true,
      padding: 40,
      idealEdgeLength: 110,
      nodeRepulsion: 7000,
    },
  });

  cy.on("tap", "node", (event) => {
    renderNode(event.target.data(), graph.material[event.target.id()] || []);
  });

  clusterSelect.addEventListener("change", () => {
    highlightCluster(cy, graph, clusterSelect.value);
  });
})();

function highlightCluster(cy, graph, clusterId) {
  cy.elements().removeClass("faded clusterEdge clusterNode");
  if (!clusterId) {
    return;
  }

  const cluster = graph.clusters.find((item) => item.id === clusterId);
  if (!cluster) {
    return;
  }

  cy.elements().addClass("faded");
  for (const relationId of cluster.relations) {
    const edge = cy.getElementById(relationId);
    if (edge.empty()) {
      continue;
    }
    edge.removeClass("faded").addClass("clusterEdge");
    edge.source().removeClass("faded").addClass("clusterNode");
    edge.target().removeClass("faded").addClass("clusterNode");
  }
}

function renderNode(node, material) {
  const details = document.getElementById("details");
  details.innerHTML = "";

  const title = document.createElement("h2");
  title.textContent = node.label;
  details.appendChild(title);

  const kind = document.createElement("p");
  kind.className = "muted";
  kind.textContent = `${node.kind} · ${node.id}`;
  details.appendChild(kind);

  const propsSection = section("Props");
  const props = document.createElement("pre");
  props.textContent = JSON.stringify(node.props || {}, null, 2);
  propsSection.appendChild(props);
  details.appendChild(propsSection);

  const materialSection = section("Material");
  if (material.length === 0) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "No material attached.";
    materialSection.appendChild(empty);
  } else {
    const list = document.createElement("ul");
    for (const item of material) {
      const row = document.createElement("li");
      const label = item.label || item.id;
      const body = item.has_body ? "inline body" : "no inline body";
      const path = item.path ? ` · ${item.path}` : "";
      row.textContent = `${label} · ${item.kind} · ${item.lang || "no language"} · ${body}${path}`;
      list.appendChild(row);
    }
    materialSection.appendChild(list);
  }
  details.appendChild(materialSection);
}

function renderError(message) {
  const details = document.getElementById("details");
  details.innerHTML = "";
  const title = document.createElement("h2");
  title.textContent = "Could not load graph";
  const body = document.createElement("pre");
  body.textContent = message;
  details.appendChild(title);
  details.appendChild(body);
}

function section(titleText) {
  const wrapper = document.createElement("div");
  wrapper.className = "section";
  const title = document.createElement("h3");
  title.textContent = titleText;
  wrapper.appendChild(title);
  return wrapper;
}
