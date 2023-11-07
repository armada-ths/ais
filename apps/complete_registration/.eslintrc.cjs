module.exports = {
    root: true,
    env: { browser: true, es2020: true },
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:react-hooks/recommended"
    ],
    ignorePatterns: ["dist", ".eslintrc.cjs"],
    parser: "@typescript-eslint/parser",
    plugins: ["react-refresh", "prefer-function-declarations"],
    rules: {
        "prefer-function-declarations/prefer-function-declarations": "error",
        "react-refresh/only-export-components": [
            "warn",
            { allowConstantExport: true }
        ]
    }
}
