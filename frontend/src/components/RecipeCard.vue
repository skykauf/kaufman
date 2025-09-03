<template>
  <v-card class="recipe-card" v-if="recipe.recipe_name">
    <!-- Recipe Header -->
    <div class="recipe-header">
      <h2 class="recipe-title">{{ recipe.recipe_name }}</h2>
      <div class="flex justify-center gap-6 flex-wrap">
        <div class="flex items-center gap-2 text-white/90">
          <v-icon size="20" color="white">mdi-clock-outline</v-icon>
          <span class="text-sm">{{ recipe.cooking_time }}</span>
        </div>
        <div class="flex items-center gap-2 text-white/90" v-if="recipe.servings">
          <v-icon size="20" color="white">mdi-account-group</v-icon>
          <span class="text-sm">{{ recipe.servings }} servings</span>
        </div>
        <div class="flex items-center gap-2 text-white/90" v-if="recipe.difficulty">
          <v-icon size="20" color="white">mdi-chart-line</v-icon>
          <span class="text-sm capitalize">{{ recipe.difficulty }}</span>
        </div>
        <div class="flex items-center gap-2 text-white/90" v-if="recipe.cuisine_type && recipe.cuisine_type !== 'unknown'">
          <v-icon size="20" color="white">mdi-earth</v-icon>
          <span class="text-sm capitalize">{{ recipe.cuisine_type }}</span>
        </div>
      </div>
    </div>

    <!-- Recipe Images -->
    <div class="bg-gray-50 p-6 flex gap-4 justify-center flex-wrap" v-if="recipe.front_image">
      <div class="relative rounded-2xl overflow-hidden shadow-lg">
        <img 
          :src="getGitHubImageUrl(recipe.front_image)" 
          :alt="`${recipe.recipe_name} - Front`"
          class="w-48 h-36 object-cover"
          @error="handleImageError"
        />
        <div class="absolute bottom-0 left-0 right-0 bg-black/70 text-white p-2 text-center text-sm font-semibold">
          Front
        </div>
      </div>
      <div class="relative rounded-2xl overflow-hidden shadow-lg" v-if="recipe.back_image">
        <img 
          :src="getGitHubImageUrl(recipe.back_image)" 
          :alt="`${recipe.recipe_name} - Back`"
          class="w-48 h-36 object-cover"
          @error="handleImageError"
        />
        <div class="absolute bottom-0 left-0 right-0 bg-black/70 text-white p-2 text-center text-sm font-semibold">
          Back
        </div>
      </div>
    </div>

    <!-- Recipe Content -->
    <div class="p-6">
      <!-- Ingredients Section -->
      <div class="mb-8">
        <h3 class="flex items-center gap-3 text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-gray-200">
          <v-icon size="24" color="primary">mdi-food-variant</v-icon>
          Ingredients
        </h3>
        <div class="space-y-3">
          <div 
            v-for="(ingredient, index) in recipe.ingredients" 
            :key="index" 
            class="flex items-center gap-4 p-3 bg-gray-50 rounded-xl border-l-4 border-recipe-primary"
          >
            <span class="font-semibold text-recipe-primary min-w-20">{{ ingredient.amount }}</span>
            <span class="flex-1 font-medium">{{ ingredient.item }}</span>
            <span class="text-gray-600 italic text-sm" v-if="ingredient.notes">({{ ingredient.notes }})</span>
          </div>
        </div>
      </div>

      <!-- Instructions Section -->
      <div class="mb-8">
        <h3 class="flex items-center gap-3 text-xl font-bold text-gray-800 mb-4 pb-2 border-b-2 border-gray-200">
          <v-icon size="24" color="primary">mdi-format-list-numbered</v-icon>
          Instructions
        </h3>
        <ol class="space-y-4 pl-6">
          <li 
            v-for="(instruction, index) in recipe.instructions" 
            :key="index" 
            class="text-gray-700 leading-relaxed"
          >
            {{ instruction }}
          </li>
        </ol>
      </div>

      <!-- Notes Section -->
      <div v-if="recipe.notes" class="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
        <h3 class="flex items-center gap-3 text-lg font-bold text-yellow-800 mb-2">
          <v-icon size="20" color="warning">mdi-lightbulb</v-icon>
          Notes
        </h3>
        <p class="text-yellow-700 leading-relaxed">{{ recipe.notes }}</p>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  name: 'RecipeCard',
  props: {
    recipe: {
      type: Object,
      required: true
    }
  },
  methods: {
    getGitHubImageUrl(imageName) {
      return `https://github.com/skykauf/kaufman/raw/refs/heads/main/mimi_recipe_pictures/${imageName}`;
    },

    handleImageError(event) {
      // Create a fallback div with recipe name
      const fallbackDiv = document.createElement('div');
      fallbackDiv.className = 'w-48 h-36 bg-gradient-to-br from-recipe-primary to-recipe-secondary rounded-2xl flex items-center justify-center';
      fallbackDiv.innerHTML = `
        <div class="text-center text-white">
          <div class="text-3xl mb-2">🍳</div>
          <div class="text-sm font-semibold leading-tight">${this.recipe.recipe_name}</div>
        </div>
      `;
      event.target.parentNode.replaceChild(fallbackDiv, event.target);
    }
  }
}
</script>

<style scoped>
.recipe-card {
  @apply bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1;
}

.recipe-header {
  @apply bg-gradient-to-br from-recipe-primary to-recipe-secondary text-white p-6 rounded-t-2xl;
}

.recipe-title {
  @apply text-3xl font-recipe font-bold mb-4 text-center drop-shadow-lg;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .recipe-title {
    @apply text-2xl;
  }
  
  .recipe-header > div {
    @apply flex-col gap-2;
  }
  
  .recipe-header > div > div {
    @apply flex-col items-start gap-1;
  }
  
  .recipe-header > div > div > div {
    @apply flex-row;
  }
}
</style>
