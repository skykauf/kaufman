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
        <div class="flex justify-between items-start mb-4">
          <div class="flex-1 mr-4">
            <v-text-field
              v-model="searchQuery"
              placeholder="Search recipes..."
              prepend-inner-icon="mdi-magnify"
              variant="outlined"
              hide-details
            />
          </div>
          <v-btn
            color="primary"
            size="large"
            @click="showUploadModal = true"
            class="px-6"
          >
            <v-icon left>mdi-camera-plus</v-icon>
            Upload Recipe Photos
          </v-btn>
        </div>
        
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

    <!-- Upload Modal -->
    <v-dialog v-model="showUploadModal" max-width="600px" persistent>
      <v-card class="rounded-2xl">
        <v-card-title class="text-2xl font-bold text-center py-6 bg-gradient-to-r from-recipe-primary to-recipe-secondary text-white">
          <v-icon left size="large">mdi-camera-plus</v-icon>
          Upload Recipe Card Photos
        </v-card-title>
        
        <v-card-text class="p-8">
          <div class="text-center mb-6">
            <p class="text-lg text-gray-600 mb-2">
              Please upload both the front and back of your recipe card
            </p>
            <p class="text-sm text-gray-500">
              Supported formats: JPG, PNG, HEIC (max 10MB each)
            </p>
          </div>

          <div class="space-y-6">
            <!-- Front Photo Upload -->
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-recipe-primary transition-colors">
              <v-icon size="48" color="grey" class="mb-4">mdi-card-text-outline</v-icon>
              <h3 class="text-lg font-semibold mb-2">Front of Recipe Card</h3>
              <input
                ref="frontFileInput"
                type="file"
                accept="image/*"
                @change="handleFrontFileSelect"
                class="hidden"
              />
              <v-btn
                v-if="!frontFile"
                color="primary"
                variant="outlined"
                @click="$refs.frontFileInput.click()"
                class="mb-2"
              >
                <v-icon left>mdi-upload</v-icon>
                Choose Front Photo
              </v-btn>
              <div v-else class="space-y-2">
                <v-chip color="success" class="mb-2">
                  <v-icon left>mdi-check</v-icon>
                  {{ frontFile.name }}
                </v-chip>
                <br>
                <v-btn
                  color="primary"
                  variant="text"
                  size="small"
                  @click="$refs.frontFileInput.click()"
                >
                  Change Photo
                </v-btn>
              </div>
            </div>

            <!-- Back Photo Upload -->
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-recipe-primary transition-colors">
              <v-icon size="48" color="grey" class="mb-4">mdi-card-text</v-icon>
              <h3 class="text-lg font-semibold mb-2">Back of Recipe Card</h3>
              <input
                ref="backFileInput"
                type="file"
                accept="image/*"
                @change="handleBackFileSelect"
                class="hidden"
              />
              <v-btn
                v-if="!backFile"
                color="primary"
                variant="outlined"
                @click="$refs.backFileInput.click()"
                class="mb-2"
              >
                <v-icon left>mdi-upload</v-icon>
                Choose Back Photo
              </v-btn>
              <div v-else class="space-y-2">
                <v-chip color="success" class="mb-2">
                  <v-icon left>mdi-check</v-icon>
                  {{ backFile.name }}
                </v-chip>
                <br>
                <v-btn
                  color="primary"
                  variant="text"
                  size="small"
                  @click="$refs.backFileInput.click()"
                >
                  Change Photo
                </v-btn>
              </div>
            </div>
          </div>

          <v-alert
            v-if="uploadError"
            type="error"
            class="mt-4"
            closable
            @click:close="uploadError = ''"
          >
            {{ uploadError }}
          </v-alert>

          <v-alert
            v-if="uploadSuccess"
            type="success"
            class="mt-4"
            closable
            @click:close="uploadSuccess = ''"
          >
            {{ uploadSuccess }}
          </v-alert>
        </v-card-text>

        <v-card-actions class="p-6 pt-0">
          <v-btn
            variant="text"
            @click="closeUploadModal"
            :disabled="uploading"
          >
            Cancel
          </v-btn>
          <v-spacer />
          <v-btn
            color="primary"
            @click="uploadPhotos"
            :disabled="!frontFile || !backFile || uploading"
            :loading="uploading"
            class="px-8"
          >
            <v-icon left>mdi-cloud-upload</v-icon>
            Upload Photos
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      ],
      // Upload modal state
      showUploadModal: false,
      frontFile: null,
      backFile: null,
      uploading: false,
      uploadError: '',
      uploadSuccess: ''
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
      const response = await fetch('https://raw.githubusercontent.com/KaufmanEnterprises/kaufman/refs/heads/main/extracted_recipes.json');
      
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
  },
  methods: {
    handleFrontFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        if (this.validateFile(file)) {
          this.frontFile = file;
          this.uploadError = '';
        }
      }
    },
    handleBackFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        if (this.validateFile(file)) {
          this.backFile = file;
          this.uploadError = '';
        }
      }
    },
    validateFile(file) {
      const maxSize = 10 * 1024 * 1024; // 10MB
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/heic', 'image/heif'];
      
      if (file.size > maxSize) {
        this.uploadError = 'File size must be less than 10MB';
        return false;
      }
      
      if (!allowedTypes.includes(file.type.toLowerCase())) {
        this.uploadError = 'Please select a valid image file (JPG, PNG, or HEIC)';
        return false;
      }
      
      return true;
    },
    async uploadPhotos() {
      if (!this.frontFile || !this.backFile) {
        this.uploadError = 'Please select both front and back photos';
        return;
      }

      this.uploading = true;
      this.uploadError = '';
      this.uploadSuccess = '';

      try {
        // Generate unique folder ID
        const folderId = `recipe_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        const formData = new FormData();
        formData.append('folder_id', folderId);
        formData.append('front_photo', this.frontFile);
        formData.append('back_photo', this.backFile);

        // Determine backend URL based on current host
        const backendUrl = window.location.hostname === 'localhost' 
          ? 'http://localhost:8000' 
          : `http://${window.location.hostname}:8000`;
        
        console.log('Uploading to:', `${backendUrl}/upload-recipe-photos`);
        
        const response = await fetch(`${backendUrl}/upload-recipe-photos`, {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error('Upload failed:', response.status, response.statusText, errorText);
          throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
        }

        const result = await response.json();
        this.uploadSuccess = `Photos uploaded successfully! Folder ID: ${result.folderId}`;
        
        // Reset form after successful upload
        setTimeout(() => {
          this.closeUploadModal();
        }, 2000);

      } catch (error) {
        console.error('Upload error:', error);
        this.uploadError = `Upload failed: ${error.message}`;
      } finally {
        this.uploading = false;
      }
    },
    closeUploadModal() {
      this.showUploadModal = false;
      this.frontFile = null;
      this.backFile = null;
      this.uploadError = '';
      this.uploadSuccess = '';
      this.uploading = false;
      
      // Reset file inputs
      if (this.$refs.frontFileInput) {
        this.$refs.frontFileInput.value = '';
      }
      if (this.$refs.backFileInput) {
        this.$refs.backFileInput.value = '';
      }
    }
  }
}
</script>

<style>
/* Custom styles can be added here if needed */
</style>
