<template>
  <div id="app">
    <header>
      <h1>Welcome to Vue.js</h1>
    </header>
    <main>
      <div class="counter-section">
        <h2>Counter: {{ count }}</h2>
        <div class="button-group">
          <button @click="increment" class="btn btn-primary">+</button>
          <button @click="decrement" class="btn btn-secondary">-</button>
          <button @click="reset" class="btn btn-reset">Reset</button>
        </div>
      </div>
      <div class="message-section">
        <input 
          v-model="message" 
          placeholder="Type a message..." 
          class="message-input"
        />
        <p class="message-display">{{ message || 'No message yet' }}</p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      count: 0,
      message: ''
    }
  },
  methods: {
    increment() {
      this.count++
    },
    decrement() {
      this.count--
    },
    reset() {
      this.count = 0
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
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

header {
  text-align: center;
  margin-bottom: 3rem;
}

h1 {
  color: white;
  font-size: 3rem;
  font-weight: 300;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

main {
  background: white;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  max-width: 500px;
  width: 100%;
}

.counter-section {
  text-align: center;
  margin-bottom: 3rem;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 60px;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-secondary {
  background: #764ba2;
  color: white;
}

.btn-reset {
  background: #f8f9fa;
  color: #333;
  border: 2px solid #dee2e6;
}

.message-section {
  text-align: center;
}

.message-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  margin-bottom: 1rem;
  transition: border-color 0.2s ease;
}

.message-input:focus {
  outline: none;
  border-color: #667eea;
}

.message-display {
  font-size: 1.1rem;
  color: #6c757d;
  font-style: italic;
}
</style>
