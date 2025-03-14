// Global variables
let nodes = [];
let ingredientNames = [];
let selectedIngredients = [];

// DOM elements
const inputContainer = document.getElementById('ingredient-input-container');
const inputElement = document.getElementById('ingredient-input');
const suggestionsElement = document.getElementById('suggestions');
const hiddenInput = document.getElementById('bannerIngredientsInput');

// Load the JSON file when the page loads
document.addEventListener('DOMContentLoaded', () => {
  loadIngredients();
  setupAutocomplete();
});

// Function to load the ingredients from JSON
function loadIngredients() {
  fetch('data/nodes.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      nodes = data;
      // Extract only node names for the autocomplete
      ingredientNames = nodes.map(node => node.name);
      console.log('Loaded', ingredientNames.length, 'ingredients');
    })
    .catch(error => {
      console.error('Error loading the JSON file:', error);
      // For testing - use sample data if the file can't be loaded
      const sampleData = [
        { "node_id": 51, "name": "acorn squash", "flavours": "['sweet', 'neutral']" },
        { "node_id": 52, "name": "apple", "flavours": "['sweet', 'tart']" },
        { "node_id": 53, "name": "asparagus", "flavours": "['bitter', 'earthy']" },
        { "node_id": 54, "name": "avocado", "flavours": "['creamy', 'nutty']" },
        { "node_id": 55, "name": "basil", "flavours": "['aromatic', 'fresh']" },
        { "node_id": 56, "name": "bell pepper", "flavours": "['sweet', 'fresh']" },
        { "node_id": 57, "name": "blueberry", "flavours": "['sweet', 'tart']" },
        { "node_id": 58, "name": "carrot", "flavours": "['sweet', 'earthy']" },
        { "node_id": 59, "name": "cilantro", "flavours": "['fresh', 'citrusy']" },
        { "node_id": 60, "name": "cinnamon", "flavours": "['sweet', 'warm']" }
      ];
      nodes = sampleData;
      ingredientNames = nodes.map(node => node.name);
      console.log('Using sample data with', ingredientNames.length, 'ingredients');
    });
}

// Function to add an ingredient tag
function addIngredient(ingredient) {
  // Check if the ingredient is valid and not already added
  if (ingredientNames.includes(ingredient) && !selectedIngredients.includes(ingredient)) {
    selectedIngredients.push(ingredient);
    renderSelectedIngredients();
    
    // Clear the input field
    inputElement.value = '';
    
    // Hide suggestions
    suggestionsElement.style.display = 'none';
    
    // Update the hidden input with comma-separated values
    updateHiddenInput();
    
    return true;
  }
  return false;
}

// Function to remove an ingredient from the selected list
function removeIngredient(ingredient) {
  const index = selectedIngredients.indexOf(ingredient);
  if (index !== -1) {
    selectedIngredients.splice(index, 1);
    renderSelectedIngredients();
    updateHiddenInput();
  }
}

// Function to render the selected ingredients as inline tags
function renderSelectedIngredients() {
  // Clear existing tags
  const existingTags = inputContainer.querySelectorAll('.ingredient-tag');
  existingTags.forEach(tag => tag.remove());
  
  // Add tags before the input element
  selectedIngredients.forEach(ingredient => {
    const tag = document.createElement('span');
    tag.classList.add('ingredient-tag');
    
    const text = document.createElement('span');
    text.textContent = ingredient;
    
    const removeBtn = document.createElement('span');
    removeBtn.classList.add('remove-tag');
    removeBtn.innerHTML = '&times;';
    removeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      removeIngredient(ingredient);
    });
    
    tag.appendChild(text);
    tag.appendChild(removeBtn);
    
    // Insert before the input element
    inputContainer.insertBefore(tag, inputElement);
  });
  
  // Focus input after adding tags
  inputElement.focus();
}

// Function to update the hidden input with comma-separated values
function updateHiddenInput() {
  hiddenInput.value = selectedIngredients.join(', ');
}

// Set up the autocomplete functionality
function setupAutocomplete() {
  // Click on container focuses the input
  inputContainer.addEventListener('click', function(e) {
    if (e.target === inputContainer) {
      inputElement.focus();
    }
  });

  // Input event for when the user types
  inputElement.addEventListener('input', function() {
    const inputValue = this.value.toLowerCase();
    
    // Clear previous suggestions
    suggestionsElement.innerHTML = '';
    
    // Hide suggestions if input is empty
    if (inputValue.length === 0) {
      suggestionsElement.style.display = 'none';
      return;
    }
    
    // Filter ingredients based on input, excluding already selected ones
    const matchingIngredients = ingredientNames.filter(name => 
      name.toLowerCase().includes(inputValue) && !selectedIngredients.includes(name)
    );
    
    // Show suggestions if we have matches
    if (matchingIngredients.length > 0) {
      suggestionsElement.style.display = 'block';
      
      // Create and append suggestion items
      matchingIngredients.forEach(ingredient => {
        const item = document.createElement('div');
        item.classList.add('suggestion-item');
        item.textContent = ingredient;
        
        // Add click event to suggestion items
        item.addEventListener('click', function() {
          addIngredient(this.textContent);
        });
        
        suggestionsElement.appendChild(item);
      });
    } else {
      suggestionsElement.style.display = 'none';
    }
  });
  
  // Close suggestions when clicking outside
  document.addEventListener('click', function(e) {
    const isClickInsideContainer = inputContainer.contains(e.target);
    const isClickInsideSuggestions = suggestionsElement.contains(e.target);
    
    if (!isClickInsideContainer && !isClickInsideSuggestions) {
      suggestionsElement.style.display = 'none';
    }
  });
  
  // Handle keyboard navigation and Enter key to add ingredient
  inputElement.addEventListener('keydown', function(e) {
    // Handle backspace to remove the last tag when input is empty
    if (e.key === 'Backspace' && inputElement.value === '' && selectedIngredients.length > 0) {
      removeIngredient(selectedIngredients[selectedIngredients.length - 1]);
      return;
    }
    
    const items = suggestionsElement.querySelectorAll('.suggestion-item');
    
    // If Enter pressed with no suggestions but valid input, add it
    if (e.key === 'Enter' && inputElement.value.trim() !== '') {
      e.preventDefault();
      if (ingredientNames.includes(inputElement.value.trim())) {
        addIngredient(inputElement.value.trim());
        return;
      }
    }
    
    if (!items.length) return;
    
    const key = e.key;
    let activeItem = suggestionsElement.querySelector('.active');
    const activeIndex = Array.from(items).indexOf(activeItem);
    
    // Handle arrow down
    if (key === 'ArrowDown') {
      e.preventDefault();
      if (activeItem) {
        // Move to next item
        const nextIndex = (activeIndex + 1) % items.length;
        activeItem.classList.remove('active');
        items[nextIndex].classList.add('active');
      } else {
        // Activate first item if none is active
        items[0].classList.add('active');
      }
    }
    
    // Handle arrow up
    else if (key === 'ArrowUp') {
      e.preventDefault();
      if (activeItem) {
        // Move to previous item
        const prevIndex = (activeIndex - 1 + items.length) % items.length;
        activeItem.classList.remove('active');
        items[prevIndex].classList.add('active');
      } else {
        // Activate last item if none is active
        items[items.length - 1].classList.add('active');
      }
    }
    
    // Handle Enter key
    else if (key === 'Enter') {
      e.preventDefault();
      if (activeItem) {
        addIngredient(activeItem.textContent);
      }
    }
    
    // Handle comma key to add an ingredient
    else if (key === ',') {
      e.preventDefault();
      const value = inputElement.value.trim();
      if (value !== '' && ingredientNames.includes(value)) {
        addIngredient(value);
      }
    }
    
    // Handle Escape key
    else if (key === 'Escape') {
      suggestionsElement.style.display = 'none';
    }
  });
}