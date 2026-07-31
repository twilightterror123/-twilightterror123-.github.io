/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        twilight: {
          bg: "#0b0e14",
          surface: "#141a24",
          border: "#2a3342",
          text: "#e8edf5",
          muted: "#8892a8",
          accent: "#a78bfa",
        }
      }
    },
  },
  plugins: [],
}
