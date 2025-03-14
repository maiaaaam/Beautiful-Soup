let nodes = [];
let selectedNodes = [];

// DOM elements
const tagContainer = document.getElementById("tagContainer");
const autocompleteInput = document.getElementById("autocompleteInput");
const autocompleteList = document.getElementById("autocompleteList");
const bannerIngredientsInput = document.getElementById(
  "bannerIngredientsInput"
);
const selectedValues = document.getElementById("selectedValues");

// Fetch and load the nodes data
fetch("data/nodes.json")
  .then((response) => response.json())
  .then((data) => {
    nodes = data;
    console.log("Loaded nodes:", nodes.length);
  })
  .catch((error) => {
    console.error("Error loading nodes data:", error);
    // Provide sample data for demonstration if fetch fails
    nodes = [
      { node_id: 51, name: "acorn squash", flavours: "['sweet', 'neutral']" },
      { node_id: 52, name: "apple", flavours: "['sweet', 'tart']" },
      { node_id: 53, name: "asparagus", flavours: "['bitter', 'grassy']" },
      { node_id: 54, name: "avocado", flavours: "['creamy', 'nutty']" },
      { node_id: 55, name: "banana", flavours: "['sweet']" },
      { node_id: 56, name: "basil", flavours: "['herbal', 'aromatic']" },
      { node_id: 57, name: "bell pepper", flavours: "['sweet', 'crunchy']" },
      { node_id: 58, name: "blueberry", flavours: "['sweet', 'tart']" },
    ];
  });

// Function to show autocomplete suggestions
function showSuggestions(input) {
  const inputValue = input.toLowerCase();
  autocompleteList.innerHTML = "";

  if (inputValue.length === 0) {
    autocompleteList.style.display = "none";
    return;
  }

  const filteredNodes = nodes.filter(
    (node) =>
      node.name.toLowerCase().includes(inputValue) &&
      !selectedNodes.includes(node.name)
  );

  if (filteredNodes.length === 0) {
    autocompleteList.style.display = "none";
    return;
  }

  filteredNodes.forEach((node) => {
    const item = document.createElement("div");
    item.classList.add("autocomplete-item");
    item.textContent = node.name;

    item.addEventListener("click", () => {
      addTag(node.name);
      autocompleteInput.value = "";
      autocompleteList.style.display = "none";
    });

    autocompleteList.appendChild(item);
  });

  autocompleteList.style.display = "block";
}

// Function to add a tag
function addTag(nodeName) {
  if (selectedNodes.includes(nodeName)) return;

  selectedNodes.push(nodeName);

  const tag = document.createElement("div");
  tag.classList.add("node-tag");

  const tagText = document.createTextNode(nodeName);
  tag.appendChild(tagText);

  const removeButton = document.createElement("span");
  removeButton.classList.add("remove-tag");
  removeButton.innerHTML = "×";
  removeButton.addEventListener("click", () => removeTag(tag, nodeName));

  tag.appendChild(removeButton);
  tagContainer.appendChild(tag);

  updateHiddenInput();
}

// Function to remove a tag
function removeTag(tagElement, nodeName) {
  tagContainer.removeChild(tagElement);
  selectedNodes = selectedNodes.filter((node) => node !== nodeName);
  updateHiddenInput();
}

// Function to update the hidden input with comma-separated values
function updateHiddenInput() {
  const commaSeparatedValues = selectedNodes.join(",");
  bannerIngredientsInput.value = commaSeparatedValues;
  selectedValues.textContent = commaSeparatedValues;
}

// Event listeners
autocompleteInput.addEventListener("input", () => {
  showSuggestions(autocompleteInput.value);
});

autocompleteInput.addEventListener("focus", () => {
  if (autocompleteInput.value.length > 0) {
    showSuggestions(autocompleteInput.value);
  }
});

// Close the autocomplete list when clicking outside
document.addEventListener("click", (e) => {
  if (e.target !== autocompleteInput && e.target !== autocompleteList) {
    autocompleteList.style.display = "none";
  }
});
