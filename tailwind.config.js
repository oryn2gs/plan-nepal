/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        mainColor: "#fcfcfc",
        primaryColor: "#fff",
        accentColor: "#62E6B9",
        fontMainColor: "#31295F",
        fontPrimaryColor: "#3B336A",
      },
      fontFamily: {
        sans: ["Bubblegum Sans", "sans-serif"],
        serif: ["Merriweather", "serif"],
      },
      fontSize: {
        logoHeader: "1.25em", // 20 px
        mainHeader: "4.37em", // 70px
        sectionHeader: "2.5em", // 40 px
        smallHeader: "1.37em", // 22px
        regular: "1em",
        smallText: "0.87em", // 14px

        mainHeaderMb: "2.5em", // 40 px
        sectionHeader: "2em", // 32px
        smallHeader: "1.12em", // 18px
        regular: "1em",
        smallText: "0.75em", // 14px
      },
      screens: {
        sm: "480px",
        md: "744px",
        lg: "1024px",
        xl: "1280px",
      },
    },
  },
  plugins: [],
};
