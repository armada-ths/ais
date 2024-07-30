import { Toaster } from "@/components/ui/sonner.tsx"
import { TooltipProvider } from "@/components/ui/tooltip.tsx"
import { RegisterScreen } from "@/screens/register/screen.tsx"
import { RegisterCompanyUserScreen } from "@/screens/register_user/screen.tsx"
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
import "./input.css"
import { DashboardScreen } from "./screens/dashboard/screen.tsx"
import { FormScreen } from "./screens/form/screen.tsx"
import { FinalRegistrationThankYouScreen } from "./screens/fr_thank_you/screen.tsx"
import { InfoScreen } from "./shared/InfoScreen.tsx"

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

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <TooltipProvider>
            <QueryClientProvider client={queryClient}>
                <Toaster />
                <RouterProvider router={router} />
            </QueryClientProvider>
        </TooltipProvider>
    </React.StrictMode>
)
