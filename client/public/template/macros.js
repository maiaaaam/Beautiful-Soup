// macros.js

// Function to create and render charts inside a given container using Chart.js
function createCharts(nutritionData, container) {
  // Create a container for charts similar to your current layout
  const chartContainer = document.createElement("div");
  chartContainer.className = "chart-container";
  chartContainer.style.display = "flex";
  chartContainer.style.flexWrap = "wrap";
  chartContainer.style.gap = "25px";
  chartContainer.style.justifyContent = "space-between";

  // Helper function to create a chart wrapper and canvas
  function createChartWrapper(canvasId) {
    const wrapper = document.createElement("div");
    wrapper.className = "chart-wrapper";
    wrapper.style.flex = "1 1 450px";
    wrapper.style.minHeight = "340px";
    wrapper.style.marginBottom = "25px";
    wrapper.style.borderRadius = "8px";
    wrapper.style.padding = "15px";
    wrapper.style.backgroundColor = "#fdfdfd";
    wrapper.style.boxShadow = "0 2px 12px rgba(0, 0, 0, 0.04)";
    const canvas = document.createElement("canvas");
    canvas.id = canvasId;
    wrapper.appendChild(canvas);
    return { wrapper, canvas };
  }

  // Create wrappers and canvases for each chart
  const { wrapper: macroWrapper, canvas: macroCanvas } = createChartWrapper(
    "macronutrientsModal"
  );
  const { wrapper: fatWrapper, canvas: fatCanvas } =
    createChartWrapper("fatBreakdownModal");
  const { wrapper: mineralsWrapper, canvas: mineralsCanvas } =
    createChartWrapper("mineralsModal");
  const { wrapper: vitaminsWrapper, canvas: vitaminsCanvas } =
    createChartWrapper("vitaminsModal");

  // Append all wrappers to the chart container
  chartContainer.append(
    macroWrapper,
    fatWrapper,
    mineralsWrapper,
    vitaminsWrapper
  );
  container.appendChild(chartContainer);

  // Define color palettes similar to your HTML file
  const colors = {
    macros: ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899"],
    fats: ["#F97316", "#F59E0B", "#EAB308"],
    minerals: ["#06B6D4", "#0EA5E9", "#3B82F6", "#6366F1"],
    vitamins: ["#8B5CF6", "#A855F7", "#D946EF", "#EC4899"],
  };

  // Chart 1: Macronutrients Distribution (Doughnut)
  new Chart(macroCanvas, {
    type: "doughnut",
    data: {
      labels: ["Protein", "Carbohydrates", "Fat", "Fiber", "Sugar"],
      datasets: [
        {
          data: [
            nutritionData["Protein"].amount,
            nutritionData["Carbohydrates"].amount,
            nutritionData["Fat"].amount,
            nutritionData["Fiber"].amount,
            nutritionData["Sugar"].amount,
          ],
          backgroundColor: colors.macros,
          borderWidth: 1,
          borderColor: "#ffffff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right" },
        title: {
          display: true,
          text: "Macronutrients Distribution (g)",
          font: { size: 16, weight: "500" },
          color: "#2D3748",
          padding: { bottom: 15 },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              const value = context.raw || 0;
              let calories = 0;
              if (label === "Protein" || label === "Carbohydrates") {
                calories = value * 4;
              } else if (label === "Fat") {
                calories = value * 9;
              } else if (label === "Fiber" || label === "Sugar") {
                calories = value * 4;
              }
              const percentage = (
                (calories / nutritionData.Calories.amount) *
                100
              ).toFixed(1);
              return `${label}: ${value.toFixed(1)}g (${calories.toFixed(
                0
              )} kcal, ${percentage}%)`;
            },
          },
        },
      },
    },
  });

  // Chart 2: Fat Breakdown (Pie)
  new Chart(fatCanvas, {
    type: "pie",
    data: {
      labels: ["Saturated Fat", "Mono Unsaturated Fat", "Poly Unsaturated Fat"],
      datasets: [
        {
          data: [
            nutritionData["Saturated Fat"].amount,
            nutritionData["Mono Unsaturated Fat"].amount,
            nutritionData["Poly Unsaturated Fat"].amount,
          ],
          backgroundColor: colors.fats,
          borderWidth: 1,
          borderColor: "#ffffff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right" },
        title: {
          display: true,
          text: "Fat Distribution (g)",
          font: { size: 16, weight: "500" },
          color: "#2D3748",
          padding: { bottom: 15 },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              const value = context.raw || 0;
              const calories = value * 9;
              const percentage = (
                (calories / nutritionData.Calories.amount) *
                100
              ).toFixed(1);
              return `${label}: ${value.toFixed(1)}g (${calories.toFixed(
                0
              )} kcal, ${percentage}%)`;
            },
          },
        },
      },
    },
  });

  // Chart 3: Minerals (Bar)
  new Chart(mineralsCanvas, {
    type: "bar",
    data: {
      labels: ["Sodium", "Potassium", "Calcium", "Iron"],
      datasets: [
        {
          label: "Amount",
          data: [
            nutritionData["Sodium"].amount,
            nutritionData["Potassium"].amount,
            nutritionData["Calcium"].amount,
            nutritionData["Iron"].amount,
          ],
          backgroundColor: colors.minerals,
          borderWidth: 0,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: "Minerals (mg)",
          font: { size: 16, weight: "500" },
          color: "#2D3748",
          padding: { bottom: 15 },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const value = context.raw || 0;
              return `Amount: ${value.toFixed(1)} mg`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: { display: true, text: "Amount (mg)" },
        },
        x: { grid: { display: false } },
      },
    },
  });

  // Chart 4: Vitamins (Polar Area)
  new Chart(vitaminsCanvas, {
    type: "polarArea",
    data: {
      labels: ["Vitamin A (IU/100)", "Vitamin C", "Vitamin D", "Vitamin B12"],
      datasets: [
        {
          label: "Amount",
          data: [
            nutritionData["Vitamin A"].amount / 100, // scaled down for visualization
            nutritionData["Vitamin C"].amount,
            nutritionData["Vitamin D"].amount,
            nutritionData["Vitamin B12"].amount,
          ],
          backgroundColor: colors.vitamins.map((color) => color + "B3"),
          borderWidth: 1,
          borderColor: colors.vitamins,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right" },
        title: {
          display: true,
          text: "Vitamins (varied units)",
          font: { size: 16, weight: "500" },
          color: "#2D3748",
          padding: { bottom: 15 },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label || "";
              let value = context.raw || 0;
              let unit = "";
              if (label.includes("A")) {
                value = value * 100; // restore original value
                unit = "IU";
              } else if (label.includes("C")) {
                unit = "mg";
              } else if (label.includes("D")) {
                unit = "µg";
              } else if (label.includes("B12")) {
                unit = "µg";
              }
              return `${label}: ${value.toFixed(1)} ${unit}`;
            },
          },
        },
      },
    },
  });
}

// Function to open a modal displaying the charts.
// This creates the modal if it doesn't exist, then uses createCharts() to render the graphs.
function openGraphsModal(nutritionData) {
  let modal = document.getElementById("graphsModal");
  if (!modal) {
    // Create modal overlay
    modal = document.createElement("div");
    modal.id = "graphsModal";
    modal.style.display = "none";
    modal.style.position = "fixed";
    modal.style.zIndex = "1000";
    modal.style.left = "0";
    modal.style.top = "0";
    modal.style.width = "100%";
    modal.style.height = "100%";
    modal.style.overflow = "auto";
    modal.style.backgroundColor = "rgba(0,0,0,0.5)";

    // Create modal content container
    const modalContent = document.createElement("div");
    modalContent.id = "graphsModalContent";
    modalContent.style.margin = "5% auto";
    modalContent.style.backgroundColor = "#fff";
    modalContent.style.padding = "20px";
    modalContent.style.borderRadius = "8px";
    modalContent.style.width = "90%";
    modalContent.style.position = "relative";

    // Create close button
    const closeButton = document.createElement("span");
    closeButton.innerHTML = "&times;";
    closeButton.style.position = "absolute";
    closeButton.style.top = "10px";
    closeButton.style.right = "20px";
    closeButton.style.fontSize = "30px";
    closeButton.style.cursor = "pointer";
    closeButton.addEventListener("click", () => {
      modal.style.display = "none";
    });
    modalContent.appendChild(closeButton);

    // Create a container for the charts
    const chartsContainer = document.createElement("div");
    chartsContainer.id = "chartsContainer";
    modalContent.appendChild(chartsContainer);

    modal.appendChild(modalContent);
    document.body.appendChild(modal);
  }

  // Clear any previous chart content and (re)create the charts with the provided nutritionData
  const chartsContainer = document.getElementById("chartsContainer");
  chartsContainer.innerHTML = "";
  createCharts(nutritionData, chartsContainer);

  // Show the modal
  modal.style.display = "block";
}
