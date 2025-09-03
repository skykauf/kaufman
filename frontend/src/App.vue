<template>
  <div id="app">
    <header>
      <h1>🍳 Mimi's Recipe Collection</h1>
      <p class="subtitle">Discover delicious family recipes</p>
    </header>
    
    <main>
      <div class="search-section">
        <input 
          v-model="searchQuery" 
          placeholder="Search recipes..." 
          class="search-input"
        />
        <div class="filter-controls">
          <select v-model="selectedCuisine" class="filter-select">
            <option value="">All Cuisines</option>
            <option v-for="cuisine in availableCuisines" :key="cuisine" :value="cuisine">
              {{ cuisine }}
            </option>
          </select>
          <select v-model="selectedDifficulty" class="filter-select">
            <option value="">All Difficulties</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
      </div>

      <div class="stats-section">
        <div class="stat-item">
          <span class="stat-number">{{ filteredRecipes.length }}</span>
          <span class="stat-label">Recipes</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ totalIngredients }}</span>
          <span class="stat-label">Ingredients</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{{ availableCuisines.length }}</span>
          <span class="stat-label">Cuisines</span>
        </div>
      </div>

      <div class="recipes-container">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>Loading recipes...</p>
        </div>
        
        <div v-else-if="filteredRecipes.length === 0" class="no-results">
          <h3>No recipes found</h3>
          <p>Try adjusting your search or filters</p>
        </div>
        
        <RecipeCard 
          v-for="recipe in filteredRecipes" 
          :key="recipe.recipe_name"
          :recipe="recipe"
        />
      </div>
    </main>
  </div>
</template>

<script>
import RecipeCard from './components/RecipeCard.vue'
import recipeData from './extracted_recipes.json'

export default {
  name: 'App',
  components: {
    RecipeCard
  },
  data() {
    return {
      recipes: [],
      loading: true,
      searchQuery: '',
      selectedCuisine: '',
      selectedDifficulty: ''
    }
  },
  computed: {
    filteredRecipes() {
      return this.recipes.filter(recipe => {
        if (!recipe.recipe_name) return false;
        
        const matchesSearch = this.searchQuery === '' || 
          recipe.recipe_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          recipe.ingredients?.some(ing => ing.item.toLowerCase().includes(this.searchQuery.toLowerCase()));
        
        const matchesCuisine = this.selectedCuisine === '' || 
          recipe.cuisine_type === this.selectedCuisine;
        
        const matchesDifficulty = this.selectedDifficulty === '' || 
          recipe.difficulty === this.selectedDifficulty;
        
        return matchesSearch && matchesCuisine && matchesDifficulty;
      });
    },
    availableCuisines() {
      const cuisines = this.recipes
        .filter(recipe => recipe.cuisine_type && recipe.cuisine_type !== 'unknown')
        .map(recipe => recipe.cuisine_type);
      return [...new Set(cuisines)];
    },
    totalIngredients() {
      return this.recipes.reduce((total, recipe) => {
        return total + (recipe.ingredients?.length || 0);
      }, 0);
    }
  },
  async mounted() {
    try {
      // Simulate loading time for better UX
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Filter out recipes with errors
      this.recipes = recipeData.filter(recipe => recipe.recipe_name);
      this.loading = false;
    } catch (error) {
      console.error('Error loading recipes:', error);
      this.loading = false;
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  text-align: center;
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

h1 {
  color: white;
  font-size: 3.5rem;
  font-weight: 700;
  text-shadow: 0 4px 8px rgba(0,0,0,0.3);
  margin-bottom: 0.5rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  font-weight: 300;
}

main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.search-section {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  border: 2px solid #e9ecef;
  border-radius: 15px;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-controls {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

.stats-section {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  min-width: 120px;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.recipes-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e9ecef;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.no-results h3 {
  color: #6c757d;
  margin-bottom: 0.5rem;
}

.no-results p {
  color: #adb5bd;
}

@media (max-width: 768px) {
  h1 {
    font-size: 2.5rem;
  }
  
  main {
    padding: 1rem;
  }
  
  .search-section {
    padding: 1.5rem;
  }
  
  .filter-controls {
    flex-direction: column;
  }
  
  .filter-select {
    min-width: auto;
  }
  
  .stats-section {
    gap: 1rem;
  }
  
  .stat-item {
    min-width: 100px;
    padding: 1rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}
</style>
