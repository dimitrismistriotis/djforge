/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.html',
      '*/templates/**/*.html',  // For Django templates
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
