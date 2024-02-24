// This has to be on top due to some weird circular import issue
import "./store/store"

import { Toaster } from "@/components/ui/sonner.tsx"
import { queryClient } from "@/utils/query_client.ts"
import { QueryClientProvider } from "@tanstack/react-query"
import {
    RootRoute,
    Route,
    Router,
    RouterProvider
} from "@tanstack/react-router"
import "primeicons/primeicons.css"
import "primereact/resources/primereact.min.css"
import "primereact/resources/themes/tailwind-light/theme.css"
import React from "react"
import ReactDOM from "react-dom/client"
import { Provider } from "react-redux"
import "./input.css"
import { DashboardScreen } from "./screens/dashboard/screen.tsx"
import { FormScreen } from "./screens/form/screen.tsx"
import { ThankYouScreen } from "./screens/thank_you/screen.tsx"
import { InfoScreen } from "./shared/InfoScreen.tsx"
import useLoadData from "./shared/useLoadData.tsx"
import { store } from "./store/store.ts"
import LoadingAnimation from "./utils/loading_animation/loading_animation.tsx"

const rootRoute = new RootRoute({
    errorComponent: () => <div>404</div>
})
const companyDashboard = new Route({
    path: "/",
    getParentRoute: () => companyRoute,
    component: () => <DashboardScreen />
})
const companyForm = new Route({
    path: "/form",
    getParentRoute: () => companyRoute
})
const companyFormPage = new Route({
    path: "$formKey",
    getParentRoute: () => companyForm,
    component: () => <FormScreen />
})

const companyThankYou = new Route({
    path: "/thank-you",
    getParentRoute: () => companyRoute,
    component: ThankYouScreen
})

const notFoundRoute = new Route({
    path: "*",
    getParentRoute: () => rootRoute,
    component: () => (
        <InfoScreen title="404" subText="This page doesn't exist :(" />
    )
})
const companyNotFoundRoute = new Route({
    path: "*",
    getParentRoute: () => companyRoute,
    component: () => (
        <InfoScreen title="404" subText="This page doesn't exist :(" />
    )
})

const companyRoute = new Route({
    path: "$companyId",
    getParentRoute: () => rootRoute
})

const routeTree = rootRoute.addChildren([
    // Duplicate routes but with /:companyId
    companyRoute.addChildren([
        companyDashboard,
        companyThankYou,
        companyForm.addChildren([companyFormPage]),
        companyNotFoundRoute
    ]),
    notFoundRoute
])

const router = new Router({
    routeTree,
    basepath: "/dashboard"
})
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router
    }
}

export function IndexMainLogicWrapper() {
    const { initialized } = useLoadData()
    if (!initialized) return <LoadingAnimation />
    return <RouterProvider router={router} />
}

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <Provider store={store}>
                <Toaster />
                <IndexMainLogicWrapper />
            </Provider>
        </QueryClientProvider>
    </React.StrictMode>
)
