/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0b1a2e",
        secondary: "#122b45",
        highlight: "#61dafb",
        danger: "#dc3545",
        accent: "#1976d2",
      },
      fontFamily: {
        body: ['Segoe UI', 'Tahoma', 'Arial', 'sans-serif'],
      },
      borderRadius: {
        'lg': '8px',
      },
      boxShadow: {
        'custom': '0 2px 8px rgba(0,0,0,0.3)',
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-in forwards',
        'slide-in-up': 'slideInUp 0.6s ease-in-out forwards',
        'slide-in': 'slideIn 0.6s ease-in-out forwards',
        'move-buildings': 'moveBuildings 90s linear infinite',
        'move-smog': 'moveSmog 120s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        moveBuildings: {
          '0%': { transform: 'translateX(0%)' },
          '100%': { transform: 'translateX(-100%)' },
        },
        moveSmog: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
    },
  },
  plugins: [],
}
