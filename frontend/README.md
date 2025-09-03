# 🍳 Mimi's Recipe Collection

A beautiful Vue.js application to display and browse family recipes with images.

## Features

- **Recipe Display**: Beautiful cards showing recipe details including ingredients, instructions, and cooking times
- **Search & Filter**: Search recipes by name or ingredients, filter by cuisine type and difficulty
- **Image Support**: Display front and back images of recipe cards
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, modern interface with smooth animations and hover effects

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

## Recipe Data Structure

The application reads recipe data from `src/extracted_recipes.json`. Each recipe has the following structure:

```json
{
  "recipe_name": "Recipe Name",
  "ingredients": [
    {
      "item": "ingredient name",
      "amount": "quantity",
      "notes": "optional notes"
    }
  ],
  "instructions": [
    "Step 1: First instruction",
    "Step 2: Second instruction"
  ],
  "cooking_time": "time description",
  "servings": "number of servings",
  "difficulty": "easy|medium|hard",
  "cuisine_type": "cuisine name",
  "dietary_info": [],
  "notes": "additional notes",
  "front_image": "image_filename.jpg",
  "back_image": "image_filename.jpg"
}
```

## Image Setup

### Using Real Images

1. Convert your HEIC images to JPEG format
2. Place the JPEG files in `public/mimi_recipe_pictures/`
3. Update the recipe data to reference the correct image filenames

### Using Placeholder Images

The application includes SVG placeholder images for testing. These are automatically used if the referenced images are not found.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── RecipeCard.vue      # Individual recipe display component
│   ├── App.vue                 # Main application component
│   ├── main.js                 # Application entry point
│   └── extracted_recipes.json # Recipe data
├── public/
│   └── mimi_recipe_pictures/  # Recipe images
└── package.json
```

## Customization

### Styling

The application uses CSS with modern design principles:
- Gradient backgrounds
- Card-based layout
- Smooth transitions and hover effects
- Responsive design with mobile-first approach

### Adding New Recipes

1. Add your recipe data to `src/extracted_recipes.json`
2. Add corresponding images to `public/mimi_recipe_pictures/`
3. The application will automatically display the new recipes

### Modifying Components

- `RecipeCard.vue`: Customize how individual recipes are displayed
- `App.vue`: Modify the main layout, search, and filtering functionality

## Browser Support

The application works in all modern browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Images Not Loading

- Ensure image files exist in `public/mimi_recipe_pictures/`
- Check that image filenames match those referenced in the recipe data
- Verify image format is supported (JPEG, PNG, SVG)

### Development Server Issues

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version`
- Ensure port 5173 is not in use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
