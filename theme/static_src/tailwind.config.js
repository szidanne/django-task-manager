/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./**/*.py",
    "./theme/static_src/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
