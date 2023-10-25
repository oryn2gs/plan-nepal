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
        fontColorAccent: "#c9c9c9",
      },
      fontFamily: {
        body: ['"Proxima Nova"', '"Roboto"', "sans"],
        header: ['"Bubblegum sans"', '"M PLUS Rounded 1c"', "sans-serif"],
      },
      fontSize: {
        logoHeader: "1.37em", // 22 px

        mainHeader: "4.37em", // 70px
        sectionHeader: "2.5em", // 40px
        smallHeader: "1.25em", // 20px
        regular: "1.125em", // 18px
        sm: "0.87em", // 14px

        mainHeaderMb: "2.5em", // 40px
        sectionHeaderMb: "2em", // 32px
        smallHeaderMb: "1.12em", // 18px
        regularMb: "1em", // 16px
        smMb: "0.75em", // 12px
      },
      gridTemplateRows: {
        7: "repeat(7, minmax(0, 1fr))",
        8: "repeat(8, minmax(0, 1fr))",
        10: "repeat(10, minmax(0, 1fr))",
        10: "repeat(10, minmax(0, 1fr))",
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
