/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Bauhaus palette — light
        'background': '#F0F0F0',
        'foreground': '#121212',
        'primary-red': '#D02020',
        'primary-blue': '#1040C0',
        'primary-yellow': '#F0C020',
        'muted': '#E0E0E0',
        // Semantic aliases
        'app-bg': '#F0F0F0',
        'sidebar-bg': '#FFFFFF',
        'card-bg': '#FFFFFF',
        'border': '#121212',
        'accent': '#D02020',
        'accent-glow': 'rgba(208, 32, 32, 0.3)',
        'text-main': '#121212',
        'text-sub': '#555555',
        // Dark mode aliases
        'dark-bg': '#0F0F0F',
        'dark-surface': '#1A1A1A',
        'dark-surface-alt': '#222222',
        'dark-border': '#E0E0E0',
        'dark-text-main': '#F0F0F0',
        'dark-text-sub': '#999999',
        'dark-muted': '#2A2A2A',
      },
      fontFamily: {
        sans: ['Outfit', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'hard-sm': '3px 3px 0px 0px #121212',
        'hard': '4px 4px 0px 0px #121212',
        'hard-md': '6px 6px 0px 0px #121212',
        'hard-lg': '8px 8px 0px 0px #121212',
        'dark-hard-sm': '3px 3px 0px 0px #E0E0E0',
        'dark-hard': '4px 4px 0px 0px #E0E0E0',
        'dark-hard-md': '6px 6px 0px 0px #E0E0E0',
        'dark-hard-lg': '8px 8px 0px 0px #E0E0E0',
      },
      keyframes: {
        'pulse-glow': {
          '0%': { boxShadow: '0 0 0 0 rgba(208, 32, 32, 0.7)' },
          '70%': { boxShadow: '0 0 0 10px rgba(208, 32, 32, 0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(208, 32, 32, 0)' },
        },
      },
      animation: {
        'pulse-glow': 'pulse-glow 1.5s infinite',
      },
    },
  },
  plugins: [],
}
