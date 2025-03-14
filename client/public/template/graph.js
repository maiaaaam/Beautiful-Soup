// let nodesData = [];
let edgesData = [];

document.addEventListener("DOMContentLoaded", () => {
  loadData();
});

function loadData() {
  fetch("data/nodes.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      nodesData = data;
    })
    .catch((error) => {
      nodesData = [];
    });

  fetch("data/edges.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      edgesData = data;
    })
    .catch((error) => {
      edgesData = [];
    });
}

// Initialize the visualization
let svg, svgGroup, simulation, nodeElements, linkElements;
let width, height;
const NUM_NEIGHBORS = 5;

// Colors for the visualization
const colors = {
  background: "#f9f9f9",
  selectedNode: "#e74c3c",
  neighborNode: "#3498db",
  selectedNodeStroke: "#c0392b",
  neighborNodeStroke: "#2980b9",
  selectedLink: "#e74c3c",
  neighborLink: "#95a5a6",
  textSelected: "#2c3e50",
  textNeighbor: "#34495e",
  tooltipBg: "rgba(44, 62, 80, 0.9)",
  tooltipText: "#ffffff",
  highlightedScore: "#2ecc71",
};

// Create legend with updated design
function createLegend() {
  const legend = d3
    .select("#graph-container")
    .append("div")
    .attr("class", "legend");

  const items = [
    {
      label: "Selected Ingredient",
      color: colors.selectedNode,
      type: "node",
    },
    {
      label: "Neighboring Ingredient",
      color: colors.neighborNode,
      type: "node",
    },
    { label: "Direct Pairing", color: colors.selectedLink, type: "link" },
    {
      label: "Neighbor Connection",
      color: colors.neighborLink,
      type: "link",
    },
  ];

  items.forEach((item) => {
    const div = legend.append("div").attr("class", "legend-item");

    if (item.type === "node") {
      div
        .append("div")
        .attr("class", "legend-color")
        .style("background-color", item.color);
    } else {
      div
        .append("div")
        .attr("class", "legend-line")
        .style("background-color", item.color);
    }

    div.append("span").text(item.label);
  });
}

// Initialize the visualization container with enhanced styling
function initVisualization() {
  // Clear any existing SVG
  d3.select("#graph-container svg").remove();

  // Get container dimensions
  const container = document.getElementById("graph-container");
  width = container.clientWidth;
  height = container.clientHeight;

  // Create SVG with gradient background
  svg = d3
    .select("#graph-container")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  // Create a group for the graph that will be transformed during zoom
  svgGroup = svg.append("g");

  // Add enhanced zoom behavior with smoother transitions
  const zoom = d3
    .zoom()
    .scaleExtent([0.1, 4])
    .on("zoom", (event) => {
      svgGroup.attr("transform", event.transform);
    });

  svg.call(zoom).call(zoom.transform, d3.zoomIdentity);

  // Create the tooltip with enhanced styling
  const tooltip = d3.select(".tooltip");

  // Create legend if it doesn't exist
  if (!document.querySelector(".legend")) {
    createLegend();
  }
}

// Process the data and create the subgraph
function createSubgraph(ingredientList) {
  const recipeGrid = document.querySelector(".recipe-grid");
  const cardHTML = `
    <div class="recipe-card">
      <div id="graph-container">
        <div class="tooltip"></div>
      </div>
    </div>
  `;
  recipeGrid.insertAdjacentHTML("beforeend", cardHTML);

  // Convert ingredient names to lowercase for case-insensitive matching
  const lowercaseIngredients = ingredientList.map((ing) =>
    ing.toLowerCase().trim()
  );

  // Find node IDs for the selected ingredients
  const ingredientIds = nodesData
    .filter((node) => lowercaseIngredients.includes(node.name.toLowerCase()))
    .map((node) => node.node_id);

  if (ingredientIds.length === 0) {
    alert("None of the entered ingredients were found in the database.");
    return null;
  }

  // Create a full graph representation
  const graph = { nodes: {}, edges: {} };

  // Add all nodes
  nodesData.forEach((node) => {
    graph.nodes[node.node_id] = {
      id: node.node_id,
      name: node.name,
      neighbors: [],
    };
  });

  // Add all edges and collect neighbors
  edgesData.forEach((edge) => {
    // Store the edge
    const edgeId = `${Math.min(edge.id_1, edge.id_2)}-${Math.max(
      edge.id_1,
      edge.id_2
    )}`;
    graph.edges[edgeId] = {
      source: edge.id_1,
      target: edge.id_2,
      score: edge.score,
    };

    // Add to neighbors
    graph.nodes[edge.id_1].neighbors.push({
      id: edge.id_2,
      score: edge.score,
    });

    graph.nodes[edge.id_2].neighbors.push({
      id: edge.id_1,
      score: edge.score,
    });
  });

  // Get the subgraph nodes and edges
  const subgraphNodeIds = new Set(ingredientIds);

  // Add top neighbors for each selected ingredient
  ingredientIds.forEach((nodeId) => {
    const node = graph.nodes[nodeId];
    if (!node) return;

    // Sort neighbors by score
    const sortedNeighbors = [...node.neighbors]
      .sort((a, b) => b.score - a.score)
      .slice(0, NUM_NEIGHBORS);

    // Add to subgraph
    sortedNeighbors.forEach((neighbor) => {
      subgraphNodeIds.add(neighbor.id);
    });
  });

  // Create subgraph nodes
  const nodes = Array.from(subgraphNodeIds).map((id) => {
    const node = graph.nodes[id];
    return {
      id: node.id,
      name: node.name,
      isHighlighted: ingredientIds.includes(node.id),
    };
  });

  // Create subgraph edges
  const edgeKeys = Object.keys(graph.edges);
  const links = [];

  edgeKeys.forEach((key) => {
    const edge = graph.edges[key];
    if (subgraphNodeIds.has(edge.source) && subgraphNodeIds.has(edge.target)) {
      links.push({
        source: edge.source,
        target: edge.target,
        score: edge.score,
        isHighlighted:
          ingredientIds.includes(edge.source) &&
          ingredientIds.includes(edge.target),
      });
    }
  });

  return { nodes, links };
}

// Visualize the subgraph with enhanced aesthetics
function visualizeSubgraph(subgraph) {
  if (!subgraph) return;

  // Initialize the visualization if not already done
  if (!svg) {
    initVisualization();
  } else {
    // Clear existing elements
    svgGroup.selectAll("*").remove();
  }

  // Create links with enhanced styling and gradients
  linkElements = svgGroup
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(subgraph.links)
    .enter()
    .append("line")
    .attr("class", "link")
    .attr("stroke", (d) =>
      d.isHighlighted ? colors.selectedLink : colors.neighborLink
    )
    .attr("stroke-width", (d) => (d.isHighlighted ? 2.5 : 1 + d.score * 1.5))
    .attr("stroke-opacity", (d) =>
      d.isHighlighted ? 0.8 : 0.4 + d.score * 0.3
    )
    .attr("stroke-linecap", "round");

  // Create nodes group
  nodeElements = svgGroup
    .append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(subgraph.nodes)
    .enter()
    .append("g")
    .attr("class", "node")
    .call(
      d3
        .drag()
        .on("start", dragStarted)
        .on("drag", dragging)
        .on("end", dragEnded)
    );

  // Add enhanced node circles with better styling
  nodeElements
    .append("circle")
    .attr("r", (d) => (d.isHighlighted ? 15 : 10))
    .attr("fill", (d) =>
      d.isHighlighted ? colors.selectedNode : colors.neighborNode
    )
    .attr("stroke", (d) =>
      d.isHighlighted ? colors.selectedNodeStroke : colors.neighborNodeStroke
    )
    .attr("stroke-width", 2)
    .attr("stroke-opacity", 0.8)
    .style("filter", "drop-shadow(0px 2px 3px rgba(0,0,0,0.1))");

  // Add enhanced labels to nodes
  nodeElements
    .append("text")
    .text((d) => d.name)
    .attr("font-size", (d) => (d.isHighlighted ? "14px" : "12px"))
    .attr("dx", (d) => (d.isHighlighted ? 20 : 15))
    .attr("dy", 4)
    .attr("font-weight", (d) => (d.isHighlighted ? "600" : "500"))
    .attr("fill", (d) =>
      d.isHighlighted ? colors.textSelected : colors.textNeighbor
    )
    .style("font-family", '"Comfortaa", sans-serif')
    .style("pointer-events", "none");

  // Create enhanced tooltip events
  nodeElements
    .on("mouseover", function (event, d) {
      // Highlight connected links and nodes
      linkElements.style("opacity", (e) =>
        e.source.id === d.id || e.target.id === d.id ? 1 : 0.1
      );

      nodeElements.style("opacity", (n) =>
        n.id === d.id ||
        subgraph.links.some(
          (l) =>
            (l.source.id === d.id && l.target.id === n.id) ||
            (l.target.id === d.id && l.source.id === n.id)
        )
          ? 1
          : 0.3
      );

      // Show tooltip
      const tooltip = d3.select(".tooltip");
      tooltip.style("display", "block").html(`<strong>${d.name}</strong>`);

      // Position the tooltip
      const tooltipWidth = tooltip.node().getBoundingClientRect().width;
      tooltip
        .style("left", event.pageX - tooltipWidth / 2 + "px")
        .style("top", event.pageY - 200 + "px");

      // Scale up the node
      d3.select(this)
        .select("circle")
        .transition()
        .duration(200)
        .attr("r", d.isHighlighted ? 18 : 13);
    })
    .on("mousemove", function (event) {
      // Update tooltip position
      const tooltip = d3.select(".tooltip");
      const tooltipWidth = tooltip.node().getBoundingClientRect().width;
      tooltip
        .style("left", event.pageX - tooltipWidth / 2 + "px")
        .style("top", event.pageY - 200 + "px");
    })
    .on("mouseout", function () {
      // Reset highlights
      linkElements.style("opacity", 1);
      nodeElements.style("opacity", 1);

      // Hide tooltip
      d3.select(".tooltip").style("display", "none");

      // Reset node size
      d3.select(this)
        .select("circle")
        .transition()
        .duration(200)
        .attr("r", (d) => (d.isHighlighted ? 15 : 10));
    });

  // Enhanced link tooltips
  linkElements
    .on("mouseover", function (event, d) {
      // Highlight this link
      d3.select(this)
        .transition()
        .duration(200)
        .attr("stroke-width", d.isHighlighted ? 4 : 3)
        .attr("stroke-opacity", 0.9);

      // Find the node names
      const source = subgraph.nodes.find(
        (n) => n.id === d.source.id || n.id === d.source
      );
      const target = subgraph.nodes.find(
        (n) => n.id === d.target.id || n.id === d.target
      );

      // Show enhanced tooltip
      const tooltip = d3.select(".tooltip");
      tooltip
        .style("display", "block")
        .html(
          `<strong>${source.name}</strong> + <strong>${
            target.name
          }</strong><br>Pairing Score: <strong>${(d.score * 100).toFixed(
            0
          )}%</strong>`
        );

      // Position the tooltip
      const tooltipWidth = tooltip.node().getBoundingClientRect().width;
      tooltip
        .style("left", event.pageX - tooltipWidth / 2 + "px")
        .style("top", event.pageY - 200 + "px");
    })
    .on("mousemove", function (event) {
      // Update tooltip position
      const tooltip = d3.select(".tooltip");
      const tooltipWidth = tooltip.node().getBoundingClientRect().width;
      tooltip
        .style("left", event.pageX - tooltipWidth / 2 + "px")
        .style("top", event.pageY - 200 + "px");
    })
    .on("mouseout", function () {
      // Reset link style
      d3.select(this)
        .transition()
        .duration(200)
        .attr("stroke-width", (d) =>
          d.isHighlighted ? 2.5 : 1 + d.score * 1.5
        )
        .attr("stroke-opacity", (d) =>
          d.isHighlighted ? 0.8 : 0.4 + d.score * 0.3
        );

      // Hide tooltip
      d3.select(".tooltip").style("display", "none");
    });

  // Setup enhanced simulation with better forces
  simulation = d3
    .forceSimulation(subgraph.nodes)
    .force(
      "link",
      d3
        .forceLink(subgraph.links)
        .id((d) => d.id)
        .distance((d) => 120 - d.score * 40) // Higher score = closer nodes
        .strength((d) => 0.3 + d.score * 0.5)
    )
    .force(
      "charge",
      d3.forceManyBody().strength((d) => (d.isHighlighted ? -400 : -300))
    )
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force(
      "collision",
      d3.forceCollide().radius((d) => (d.isHighlighted ? 60 : 45))
    )
    .force("x", d3.forceX(width / 2).strength(0.05))
    .force("y", d3.forceY(height / 2).strength(0.05))
    .alphaDecay(0.02) // Slower cooling for better layout
    .on("tick", ticked);

  // Function to update positions on each tick
  function ticked() {
    linkElements
      .attr("x1", (d) => Math.max(20, Math.min(width - 20, d.source.x)))
      .attr("y1", (d) => Math.max(20, Math.min(height - 20, d.source.y)))
      .attr("x2", (d) => Math.max(20, Math.min(width - 20, d.target.x)))
      .attr("y2", (d) => Math.max(20, Math.min(height - 20, d.target.y)));

    nodeElements.attr("transform", (d) => {
      const x = Math.max(20, Math.min(width - 20, d.x));
      const y = Math.max(20, Math.min(height - 20, d.y));
      return `translate(${x}, ${y})`;
    });
  }

  // Enhanced drag functions with better transitions
  function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;

    // Visually emphasize the dragged node
    d3.select(this)
      .select("circle")
      .transition()
      .duration(200)
      .attr("r", d.isHighlighted ? 18 : 13)
      .attr("stroke-width", 3);
  }

  function dragging(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);

    // Option 1: Let nodes float freely after drag
    d.fx = null;
    d.fy = null;

    // Option 2: Keep nodes where they were dropped
    // d.fx = d.x;
    // d.fy = d.y;

    // Reset node appearance
    d3.select(this)
      .select("circle")
      .transition()
      .duration(200)
      .attr("r", d.isHighlighted ? 15 : 10)
      .attr("stroke-width", 2);
  }

  // Apply initial gentle force to spread nodes
  simulation.alpha(0.8).restart();
}

// Event listener for the visualize button
// document.getElementById("visualize-btn").addEventListener("click", function () {
//   const input = document.getElementById("bannerIngredientsInput").value;
//   if (!input) {
//     alert("Please enter at least one ingredient.");
//     return;
//   }

//   const ingredientList = input.split(",");
//   const subgraph = createSubgraph(ingredientList);
//   visualizeSubgraph(subgraph);
// });

// Also allow Enter key to trigger visualization
// document
//   .getElementById("bannerIngredientsInput")
//   .addEventListener("keyup", function (event) {
//     if (event.key === "Enter") {
//       document.getElementById("visualize-btn").click();
//     }
//   });

// Initialize the visualization on page load
// window.addEventListener("load", function () {
//   initVisualization();
//   // Optional: visualize with default data
//   // visualizeSubgraph(createSubgraph(['Tomato', 'Basil', 'Mozzarella']));
// });

// Handle window resize with smooth transitions
window.addEventListener("resize", function () {
  // Update dimensions
  const container = document.getElementById("graph-container");
  width = container.clientWidth;
  height = container.clientHeight;

  // Resize SVG
  d3.select("#graph-container svg").attr("width", width).attr("height", height);

  // Update simulation center force
  if (simulation) {
    simulation
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(width / 2).strength(0.05))
      .force("y", d3.forceY(height / 2).strength(0.05));
    simulation.alpha(0.3).restart();
  }
});
