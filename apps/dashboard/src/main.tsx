// This has to be on top due to some weird circular import issue
import "./store/store"

import { Toaster } from "@/components/ui/sonner.tsx"
import { queryClient } from "@/utils/query_client.ts"
import { QueryClientProvider } from "@tanstack/react-query"
import {
    RouterProvider,
    createRootRoute,
    createRoute,
    createRouter
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
import { FinalRegistrationThankYouScreen } from "./screens/fr_thank_you/screen.tsx"
import { InfoScreen } from "./shared/InfoScreen.tsx"
import useLoadData from "./shared/useLoadData.tsx"
import { store } from "./store/store.ts"
import LoadingAnimation from "./utils/loading_animation/loading_animation.tsx"

const rootRoute = createRootRoute({
    errorComponent: () => <div>404</div>
})
const companyDashboard = createRoute({
    path: "/",
    getParentRoute: () => companyRoute,
    component: () => <DashboardScreen />
})
const companyForm = createRoute({
    path: "/form",
    getParentRoute: () => companyRoute
})
const companyFormPage = createRoute({
    path: "$formKey",
    getParentRoute: () => companyForm,
    component: () => <FormScreen />
})
const companyFormStep = createRoute({
    path: "$formStepKey",
    getParentRoute: () => companyFormPage,
    component: () => <FormScreen />
})

const companyThankYou = createRoute({
    path: "/fr-thank-you",
    getParentRoute: () => companyRoute,
    component: FinalRegistrationThankYouScreen
})

const notFoundRoute = createRoute({
    path: "*",
    getParentRoute: () => rootRoute,
    component: () => (
        <InfoScreen title="404" subText="This page doesn't exist :(" />
    )
})
const companyNotFoundRoute = createRoute({
    path: "*",
    getParentRoute: () => companyRoute,
    component: () => (
        <InfoScreen title="404" subText="This page doesn't exist :(" />
    )
})
const root = createRoute({
    path: "/",
    getParentRoute: () => rootRoute,
    component: () => (
        <InfoScreen
            title="Armada Dasboard"
            severity="warning"
            subText="It seems like you are not logged in, this is not intended behavior. If you see this screen you should contact Armada"
        />
    )
})

const companyRoute = createRoute({
    path: "$companyId",
    getParentRoute: () => rootRoute
})

const routeTree = rootRoute.addChildren([
    root,
    companyRoute.addChildren([
        companyDashboard,
        companyThankYou,
        companyForm.addChildren([
            companyFormPage.addChildren([companyFormStep])
        ]),
        companyNotFoundRoute
    ]),
    notFoundRoute
])

const router = createRouter({
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
