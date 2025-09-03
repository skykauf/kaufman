# Vue.js Frontend

A minimal Vue.js frontend application with a modern UI.

## Getting Started

### Prerequisites

- Node.js (version 16 or higher) - We recommend Node.js 24
- npm or yarn

#### Installing Node.js with nvm (Recommended)

1. **Install nvm (Node Version Manager):**

   **On macOS/Linux:**
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
   ```

   **On Windows:**
   Download and install [nvm-windows](https://github.com/coreybutler/nvm-windows/releases)

2. **Restart your terminal or run:**
   ```bash
   source ~/.bashrc  # or source ~/.zshrc for zsh
   ```

3. **Install Node.js 24:**
   ```bash
   nvm install 24
   ```

4. **Set Node.js 24 as default:**
   ```bash
   nvm use 24
   nvm alias default 24
   ```

5. **Verify installation:**
   ```bash
   node --version  # Should show v24.x.x
   npm --version   # Should show the npm version
   ```

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

To start the development server:

```bash
npm run dev
```

This will start the development server at `http://localhost:3000` and automatically open your browser.

### Building for Production

To build the application for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

To preview the production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── index.html          # Main HTML file
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
├── src/
│   ├── main.js         # Vue app entry point
│   └── App.vue         # Main Vue component
└── README.md           # This file
```

## Technologies Used

- Vue.js 3 - Progressive JavaScript framework
- Vite - Fast build tool and dev server
- Modern CSS with gradients and animations
