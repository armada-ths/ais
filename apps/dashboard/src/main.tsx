// This has to be on top due to some weird circular import issue
import "./store/store"

import { Toaster } from "@/components/ui/sonner.tsx"
import { TooltipProvider } from "@/components/ui/tooltip.tsx"
import { RegisterScreen } from "@/screens/register/screen.tsx"
import { RegisterCompanyUserScreen } from "@/screens/register_user/screen.tsx"
import useLoadData from "@/shared/useLoadData.tsx"
import LoadingAnimation from "@/utils/loading_animation/loading_animation.tsx"
import { queryClient } from "@/utils/query_client.ts"
import { QueryClientProvider } from "@tanstack/react-query"
import {
    Outlet,
    RouterProvider,
    createRootRoute,
    createRoute,
    createRouter
} from "@tanstack/react-router"
import { TanStackRouterDevtools } from "@tanstack/router-devtools"
import "primeicons/primeicons.css"
import "primereact/resources/primereact.min.css"
import "primereact/resources/themes/tailwind-light/theme.css"
import React from "react"
import ReactDOM from "react-dom/client"
import { Provider } from "react-redux"
import ArmadaLogo from "./assets/armada_logo_green.svg"
import "./input.css"
import { DashboardScreen } from "./screens/dashboard/screen.tsx"
import { FormScreen } from "./screens/form/screen.tsx"
import { FinalRegistrationThankYouScreen } from "./screens/fr_thank_you/screen.tsx"
import { InfoScreen } from "./shared/InfoScreen.tsx"
import { store } from "./store/store.ts"

const rootRoute = createRootRoute({
    errorComponent: () => <div>404</div>,
    component: () => (
        <>
            <Outlet />
            {import.meta.env.DEV && <TanStackRouterDevtools />}
        </>
    )
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
    path: "$formPageKey",
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

const companyRegister = createRoute({
    path: "/register",
    getParentRoute: () => rootRoute,
    component: () => <RegisterScreen />
})

const companyRegisterUser = createRoute({
    path: "/register_user",
    getParentRoute: () => rootRoute,
    component: () => <RegisterCompanyUserScreen />
})

const root = createRoute({
    path: "/",
    getParentRoute: () => rootRoute,
    component: () => (
        <InfoScreen
            title="Armada Dashboard"
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
    companyRegisterUser,
    companyRegister,
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
    const { initialized, error } = useLoadData()
    if (error) {
        return (
            <section className="min-w-screen flex min-h-screen items-center justify-center">
                <div className="flex max-w-[400px] flex-col items-center">
                    <img src={ArmadaLogo} alt="Armada" className="h-52 w-52" />
                    <h1 className="mb-2 text-5xl">Could not load data</h1>
                    <p>
                        We could not load the data for you, if you are within an
                        official period at Armada such as initial registration
                        or final registration, please contact us. Otherwise
                        please come back later
                    </p>
                </div>
            </section>
        )
    }
    if (!initialized) return <LoadingAnimation />
    return <RouterProvider router={router} />
}

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <TooltipProvider>
            <QueryClientProvider client={queryClient}>
                <Provider store={store}>
                    <Toaster />
                    <IndexMainLogicWrapper />
                </Provider>
            </QueryClientProvider>
        </TooltipProvider>
    </React.StrictMode>
)
