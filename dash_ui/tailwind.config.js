/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.html',
    './app.py',
    './**/*.py',
  ],
  theme: {
    extend: {
      fontFamily: {
                sans: ['Montserrat', 'sans-serif'],
            },
    },
  },
  plugins: [],
}

