/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'app-bg': '#09090b',
        'sidebar-bg': '#101012',
        'card-bg': '#18181b',
        'border': '#27272a',
        'accent': '#8b5cf6',
        'accent-glow': 'rgba(139, 92, 246, 0.3)',
        'text-main': '#e4e4e7',
        'text-sub': '#a1a1aa',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
