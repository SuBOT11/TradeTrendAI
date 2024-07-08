const plugin = require("tailwindcss/plugin");

module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        white: "white",
        none: "none",
      },
      fontFamily: {
        quicksand: ["Quicksand", "sans-serif"],
      },
      borderWidth: {
        1: "1px",
      },
      gridTemplateRows: {
        7: "repeat(7, minmax(0, 1fr))",
        10: "repeat(8, minmax(0, 1fr))",
        8: "repeat(10, minmax(0, 1fr))",
        11: "repeat(11, minmax(0, 1fr))",
        12: "repeat(12, minmax(0, 1fr))",
      },
    },
  },
  plugins: [],
};
