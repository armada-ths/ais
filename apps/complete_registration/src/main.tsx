// This has to be on top due to some weird circular import issue
import "./store/store"

import React from "react"
import ReactDOM from "react-dom/client"
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
import { ThankYouScreen } from "./screens/thank_you/screen.tsx"
import { DashboardScreen } from "./screens/dashboard/screen.tsx"
import useLoadData from "./shared/useLoadData.tsx"

const rootRoute = new RootRoute({
    errorComponent: () => <div>404</div>
})
const dashboard = new Route({
    path: "/",
    getParentRoute: () => rootRoute,
    component: () => <DashboardScreen />
})
const form = new Route({
    path: "/form",
    getParentRoute: () => rootRoute,
    component: () => <FormScreen />
})
const thankYou = new Route({
    path: "/thank-you",
    getParentRoute: () => rootRoute,
    component: ThankYouScreen
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

export function IndexMainLogicWrapper() {
    useLoadData()
    return <RouterProvider router={router} />
}

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <Provider store={store}>
            <IndexMainLogicWrapper />
        </Provider>
    </React.StrictMode>
)
