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
      <div class="relative rounded-2xl overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform duration-200" @click="openImageModal('front')">
        <img 
          :src="getGitHubImageUrl(recipe.front_image)" 
          :alt="`${recipe.recipe_name} - Front`"
          class="w-48 h-36 object-cover"
          @error="handleImageError"
        />
        <div class="absolute bottom-0 left-0 right-0 bg-black/70 text-white p-2 text-center text-sm font-semibold">
          Front
        </div>
        <div class="absolute top-2 right-2 bg-black/50 text-white p-1 rounded-full">
          <v-icon size="16">mdi-magnify-plus</v-icon>
        </div>
      </div>
      <div class="relative rounded-2xl overflow-hidden shadow-lg cursor-pointer hover:scale-105 transition-transform duration-200" v-if="recipe.back_image" @click="openImageModal('back')">
        <img 
          :src="getGitHubImageUrl(recipe.back_image)" 
          :alt="`${recipe.recipe_name} - Back`"
          class="w-48 h-36 object-cover"
          @error="handleImageError"
        />
        <div class="absolute bottom-0 left-0 right-0 bg-black/70 text-white p-2 text-center text-sm font-semibold">
          Back
        </div>
        <div class="absolute top-2 right-2 bg-black/50 text-white p-1 rounded-full">
          <v-icon size="16">mdi-magnify-plus</v-icon>
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

    <!-- Image Modal -->
    <v-dialog v-model="showImageModal" max-width="90vw" max-height="90vh" persistent>
      <v-card class="image-modal-card">
        <v-card-title class="d-flex justify-space-between align-center pa-4">
          <span class="text-h5 font-weight-bold">{{ recipe.recipe_name }} - {{ currentImageType === 'front' ? 'Front' : 'Back' }}</span>
          <v-btn icon @click="closeImageModal" class="ml-auto">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text class="pa-0">
          <div class="image-modal-container">
            <img 
              :src="currentImageUrl" 
              :alt="`${recipe.recipe_name} - ${currentImageType === 'front' ? 'Front' : 'Back'}`"
              class="modal-image"
              @error="handleModalImageError"
            />
          </div>
        </v-card-text>
        
        <v-card-actions class="pa-4 justify-center" v-if="recipe.front_image && recipe.back_image">
          <v-btn 
            variant="outlined" 
            :disabled="currentImageType === 'front'"
            @click="switchImage('front')"
            class="mr-2"
          >
            <v-icon left>mdi-arrow-left</v-icon>
            Front
          </v-btn>
          <v-btn 
            variant="outlined" 
            :disabled="currentImageType === 'back'"
            @click="switchImage('back')"
          >
            Back
            <v-icon right>mdi-arrow-right</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
  data() {
    return {
      showImageModal: false,
      currentImageType: 'front'
    }
  },
  mounted() {
    // Add keyboard event listener for escape key
    document.addEventListener('keydown', this.handleKeydown);
  },
  beforeUnmount() {
    // Remove keyboard event listener
    document.removeEventListener('keydown', this.handleKeydown);
  },
  computed: {
    currentImageUrl() {
      if (this.currentImageType === 'front') {
        return this.getGitHubImageUrl(this.recipe.front_image);
      } else {
        return this.getGitHubImageUrl(this.recipe.back_image);
      }
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
    },

    openImageModal(imageType) {
      this.currentImageType = imageType;
      this.showImageModal = true;
    },

    closeImageModal() {
      this.showImageModal = false;
    },

    switchImage(imageType) {
      this.currentImageType = imageType;
    },

    handleModalImageError(event) {
      // Create a fallback for modal image
      const fallbackDiv = document.createElement('div');
      fallbackDiv.className = 'w-full h-96 bg-gradient-to-br from-recipe-primary to-recipe-secondary flex items-center justify-center';
      fallbackDiv.innerHTML = `
        <div class="text-center text-white">
          <div class="text-6xl mb-4">🍳</div>
          <div class="text-2xl font-semibold mb-2">${this.recipe.recipe_name}</div>
          <div class="text-lg opacity-75">${this.currentImageType === 'front' ? 'Front' : 'Back'} Image</div>
        </div>
      `;
      event.target.parentNode.replaceChild(fallbackDiv, event.target);
    },

    handleKeydown(event) {
      // Close modal on escape key press
      if (event.key === 'Escape' && this.showImageModal) {
        this.closeImageModal();
      }
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

.image-modal-card {
  @apply bg-white rounded-lg overflow-hidden;
}

.image-modal-container {
  @apply flex justify-center items-center bg-black;
  min-height: 60vh;
  max-height: 70vh;
}

.modal-image {
  @apply max-w-full max-h-full object-contain;
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

  .image-modal-container {
    min-height: 50vh;
    max-height: 60vh;
  }
}
</style>
