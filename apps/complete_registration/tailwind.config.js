import { screens } from "tailwindcss/defaultTheme"
/** @type {import('tailwindcss').Config} */
export default {
    theme: {
        extend: {},
        screens: {
            ...screens,
            "3xl": "1650px"
        }
    },
    plugins: [],
    content: ["./src/**/*.{html,js,ts,jsx,tsx}"]
}
