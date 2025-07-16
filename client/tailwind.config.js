/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'neon-pink': '#ff6b9d',
        'neon-blue': '#4ecdc4',
        'neon-green': '#a8e6cf',
        // Dark mode colors - clean blacks/grays
        'dark-bg': '#0a0a0a',
        'dark-surface': '#121212',
        'dark-card': '#1e1e1e',
        'dark-border': '#2a2a2a',
        // Darker light mode colors
        'light-bg': '#f0f2f5',
        'light-surface': '#e8eaed',
        'light-card': '#f5f6f7',
        'light-border': '#d1d5db',
        'light-text': '#1f2937',
        'light-text-muted': '#4b5563',
        'light-accent': '#e5e7eb',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-soft': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
