/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        cream: '#FFFFE3',
        'warm-brown': '#2C2416',
        rule: '#E8E0C8',
        placeholder: '#F2ECDA',
      },
      fontFamily: {
        queens: ['Queens', 'serif'],
        'queens-condensed': ['Queens Condensed', 'serif'],
      },
      width: {
        sticky: '48px',
        'sticky-expanded': '180px',
      },
    },
  },
  plugins: [],
};
