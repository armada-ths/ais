// This has to be on top due to some weird circular import issue
import "./store/store"

import React from "react"
import ReactDOM from "react-dom/client"
import { App } from "./App.tsx"
import "./input.css"
import "primereact/resources/primereact.min.css"
import "primereact/resources/themes/tailwind-light/theme.css"
import "primeicons/primeicons.css"
import { store } from "./store/store.ts"
import { Provider } from "react-redux"
import {
    Router,
    RootRoute,
    Route,
    RouterProvider
} from "@tanstack/react-router"
import { InfoScreen } from "./shared/InfoScreen.tsx"
import { FormScreen } from "./screens/form/screen.tsx"

const rootRoute = new RootRoute({
    errorComponent: () => <div>404</div>
})
const dashboard = new Route({
    path: "/",
    getParentRoute: () => rootRoute,
    component: () => <App />
})
const form = new Route({
    path: "/form",
    getParentRoute: () => rootRoute,
    component: () => <FormScreen />
})
const thankYou = new Route({
    path: "/thank-you",
    getParentRoute: () => rootRoute,
    component: () => (
        <InfoScreen
            title="You're in!"
            subText="Thank you for being a part of Armada, we look forward to seeing you at the fair"
        />
    )
})

const notFoundRoute = new Route({
    path: "*",
    getParentRoute: () => rootRoute,
    component: () => (
        <InfoScreen title="404" subText="This page doesn't exist :(" />
    )
})

const routeTree = rootRoute.addChildren([
    dashboard,
    thankYou,
    form,
    notFoundRoute
])

const router = new Router({
    routeTree
})
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router
    }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <Provider store={store}>
            <RouterProvider router={router} />
        </Provider>
    </React.StrictMode>
)
