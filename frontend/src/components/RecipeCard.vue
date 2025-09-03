<template>
  <div class="recipe-card" v-if="recipe.recipe_name">
    <div class="recipe-header">
      <h2 class="recipe-title">{{ recipe.recipe_name }}</h2>
      <div class="recipe-meta">
        <span class="meta-item">
          <i class="icon">⏱️</i>
          {{ recipe.cooking_time }}
        </span>
        <span class="meta-item" v-if="recipe.servings">
          <i class="icon">👥</i>
          {{ recipe.servings }} servings
        </span>
        <span class="meta-item" v-if="recipe.difficulty">
          <i class="icon">📊</i>
          {{ recipe.difficulty }}
        </span>
        <span class="meta-item" v-if="recipe.cuisine_type && recipe.cuisine_type !== 'unknown'">
          <i class="icon">🌍</i>
          {{ recipe.cuisine_type }}
        </span>
      </div>
    </div>

    <div class="recipe-images" v-if="recipe.front_image">
      <div class="image-container">
        <img 
          :src="getGitHubImageUrl(recipe.front_image)" 
          :alt="`${recipe.recipe_name} - Front`"
          class="recipe-image"
          @error="handleImageError"
        />
        <div class="image-label">Front</div>
      </div>
      <div class="image-container" v-if="recipe.back_image">
        <img 
          :src="getGitHubImageUrl(recipe.back_image)" 
          :alt="`${recipe.recipe_name} - Back`"
          class="recipe-image"
          @error="handleImageError"
        />
        <div class="image-label">Back</div>
      </div>
    </div>

    <div class="recipe-content">
      <div class="ingredients-section">
        <h3 class="section-title">
          <i class="icon">🥘</i>
          Ingredients
        </h3>
        <ul class="ingredients-list">
          <li v-for="(ingredient, index) in recipe.ingredients" :key="index" class="ingredient-item">
            <span class="ingredient-amount">{{ ingredient.amount }}</span>
            <span class="ingredient-name">{{ ingredient.item }}</span>
            <span class="ingredient-notes" v-if="ingredient.notes">({{ ingredient.notes }})</span>
          </li>
        </ul>
      </div>

      <div class="instructions-section">
        <h3 class="section-title">
          <i class="icon">📝</i>
          Instructions
        </h3>
        <ol class="instructions-list">
          <li v-for="(instruction, index) in recipe.instructions" :key="index" class="instruction-item">
            {{ instruction }}
          </li>
        </ol>
      </div>

      <div class="notes-section" v-if="recipe.notes">
        <h3 class="section-title">
          <i class="icon">💡</i>
          Notes
        </h3>
        <p class="notes-text">{{ recipe.notes }}</p>
      </div>
    </div>
  </div>
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
      fallbackDiv.className = 'image-fallback';
      fallbackDiv.innerHTML = `
        <div class="fallback-content">
          <div class="fallback-icon">🍳</div>
          <div class="fallback-text">${this.recipe.recipe_name}</div>
        </div>
      `;
      event.target.parentNode.replaceChild(fallbackDiv, event.target);
    }
  }
}
</script>

<style scoped>
.recipe-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.recipe-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.recipe-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.recipe-meta {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.9;
}

.icon {
  font-size: 1.1rem;
}

.recipe-images {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  justify-content: center;
  flex-wrap: wrap;
}

.image-container {
  position: relative;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.image-fallback {
  width: 200px;
  height: 150px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
}

.fallback-content {
  text-align: center;
  color: white;
}

.fallback-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.fallback-text {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.2;
}

.recipe-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  display: block;
}

.image-label {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.5rem;
  text-align: center;
  font-size: 0.8rem;
  font-weight: 600;
}

.recipe-content {
  padding: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e9ecef;
}

.ingredients-section {
  margin-bottom: 2rem;
}

.ingredients-list {
  list-style: none;
  padding: 0;
}

.ingredient-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.ingredient-amount {
  font-weight: 600;
  color: #667eea;
  min-width: 80px;
}

.ingredient-name {
  flex: 1;
  font-weight: 500;
}

.ingredient-notes {
  color: #6c757d;
  font-style: italic;
  font-size: 0.9rem;
}

.instructions-section {
  margin-bottom: 2rem;
}

.instructions-list {
  padding-left: 1.5rem;
}

.instruction-item {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #495057;
}

.notes-section {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 10px;
  padding: 1.5rem;
}

.notes-text {
  color: #856404;
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .recipe-title {
    font-size: 2rem;
  }
  
  .recipe-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .recipe-images {
    flex-direction: column;
    align-items: center;
  }
  
  .recipe-image {
    width: 100%;
    max-width: 300px;
  }
  
  .ingredient-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .ingredient-amount {
    min-width: auto;
  }
}
</style>
