<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-recipe-primary to-recipe-secondary">
    <header class="text-center py-12 px-8 bg-white/10 backdrop-blur-lg">
      <h1 class="text-5xl font-recipe font-bold text-white mb-2 drop-shadow-lg">
        🍳 Mimi's Recipe Collection
      </h1>
      <p class="text-xl text-white/90 font-light">
        Discover delicious family recipes
      </p>
    </header>
    
    <main class="flex-1 p-8 max-w-7xl mx-auto">
      <!-- Search Section -->
      <v-card class="mb-8 p-6 rounded-2xl shadow-lg">
        <v-text-field
          v-model="searchQuery"
          placeholder="Search recipes..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          class="mb-4"
          hide-details
        />
        
        <div class="flex gap-4 flex-wrap">
          <v-select
            v-model="selectedCuisine"
            :items="availableCuisines"
            label="All Cuisines"
            variant="outlined"
            class="min-w-48"
            hide-details
          />
          <v-select
            v-model="selectedDifficulty"
            :items="difficultyOptions"
            label="All Difficulties"
            variant="outlined"
            class="min-w-48"
            hide-details
          />
        </div>
      </v-card>

      <!-- Stats Section -->
      <div class="flex justify-center gap-8 mb-8 flex-wrap">
        <v-card class="text-center p-6 rounded-2xl shadow-lg min-w-32">
          <div class="text-3xl font-bold text-recipe-primary mb-2">
            {{ filteredRecipes.length }}
          </div>
          <div class="text-gray-600 font-medium">Recipes</div>
        </v-card>
        
        <v-card class="text-center p-6 rounded-2xl shadow-lg min-w-32">
          <div class="text-3xl font-bold text-recipe-primary mb-2">
            {{ totalIngredients }}
          </div>
          <div class="text-gray-600 font-medium">Ingredients</div>
        </v-card>
        
        <v-card class="text-center p-6 rounded-2xl shadow-lg min-w-32">
          <div class="text-3xl font-bold text-recipe-primary mb-2">
            {{ availableCuisines.length }}
          </div>
          <div class="text-gray-600 font-medium">Cuisines</div>
        </v-card>
      </div>

      <!-- Recipes Container -->
      <div class="space-y-8">
        <div v-if="loading" class="text-center py-16">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
            class="mb-4"
          />
          <p class="text-xl text-gray-600">Loading recipes...</p>
        </div>
        
        <div v-else-if="filteredRecipes.length === 0" class="text-center py-16">
          <v-icon size="64" color="grey" class="mb-4">mdi-food-off</v-icon>
          <h3 class="text-2xl font-bold text-gray-600 mb-2">No recipes found</h3>
          <p class="text-gray-500">Try adjusting your search or filters</p>
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
      selectedDifficulty: '',
      difficultyOptions: [
        { title: 'All Difficulties', value: '' },
        { title: 'Easy', value: 'easy' },
        { title: 'Medium', value: 'medium' },
        { title: 'Hard', value: 'hard' }
      ]
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
      return [{ title: 'All Cuisines', value: '' }, ...Array.from(new Set(cuisines)).map(c => ({ title: c, value: c }))];
    },
    totalIngredients() {
      return this.recipes.reduce((total, recipe) => {
        return total + (recipe.ingredients?.length || 0);
      }, 0);
    }
  },
  async mounted() {
    try {
      // Fetch recipes from GitHub
      const response = await fetch('https://raw.githubusercontent.com/skykauf/kaufman/refs/heads/main/extracted_recipes.json');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const recipeData = await response.json();
      
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
/* Custom styles can be added here if needed */
</style>
