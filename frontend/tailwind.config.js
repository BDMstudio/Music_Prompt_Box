/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Vaporwave palette
        'void': '#090014',
        'chrome': '#E0E0E0',
        'neon-magenta': '#FF00FF',
        'neon-cyan': '#00FFFF',
        'neon-orange': '#FF9900',
        'panel': 'rgba(26, 16, 60, 0.8)',
        'panel-solid': '#1a103c',
        'border-dim': '#2D1B4E',
        'border-glow': '#00FFFF',
        // Semantic aliases
        'app-bg': '#090014',
        'sidebar-bg': '#0d0020',
        'card-bg': 'rgba(26, 16, 60, 0.8)',
        'border': '#2D1B4E',
        'accent': '#FF00FF',
        'accent-glow': 'rgba(255, 0, 255, 0.3)',
        'text-main': '#E0E0E0',
        'text-sub': '#8888aa',
      },
      fontFamily: {
        heading: ['Orbitron', 'sans-serif'],
        mono: ['Share Tech Mono', 'monospace'],
      },
      boxShadow: {
        'neon-magenta': '0 0 10px #FF00FF',
        'neon-magenta-lg': '0 0 20px #FF00FF',
        'neon-cyan': '0 0 10px rgba(0, 255, 255, 0.5)',
        'neon-cyan-lg': '0 0 20px rgba(0, 255, 255, 0.5)',
        'neon-cyan-xl': '0 0 50px rgba(0, 255, 255, 0.2)',
        'neon-orange': '0 0 10px #FF9900',
      },
      keyframes: {
        'pulse-glow': {
          '0%': { boxShadow: '0 0 0 0 rgba(255, 0, 255, 0.7)' },
          '70%': { boxShadow: '0 0 0 10px rgba(255, 0, 255, 0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(255, 0, 255, 0)' },
        },
        'scanline-scroll': {
          '0%': { backgroundPosition: '0 0' },
          '100%': { backgroundPosition: '0 4px' },
        },
      },
      animation: {
        'pulse-glow': 'pulse-glow 1.5s infinite',
      },
    },
  },
  plugins: [],
}
