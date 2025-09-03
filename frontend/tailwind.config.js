/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'recipe-primary': '#667eea',
        'recipe-secondary': '#764ba2',
        'recipe-warm': '#ff6b6b',
        'recipe-cream': '#f8f9fa',
      },
      fontFamily: {
        'recipe': ['Playfair Display', 'serif'],
        'body': ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
