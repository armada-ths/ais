/// <reference types="vitest" />
import path from "path"
import { defineConfig } from "vitest/config"

export default defineConfig({
    test: {
        include: ["**/*.test.tsx", "**/*.test.ts"],
        globals: true
    },
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src")
        }
    }
})
