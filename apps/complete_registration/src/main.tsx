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
import ArmadaLogoGreen from "./assets/ship-green.png"

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
    getParentRoute: () => rootRoute
})
const formPage = new Route({
    path: "$formKey",
    getParentRoute: () => form,
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
    form.addChildren([formPage]),
    notFoundRoute
])

const router = new Router({
    routeTree,
    basepath: "/register"
})
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router
    }
}

export function IndexMainLogicWrapper() {
    const { initialized } = useLoadData()
    if (!initialized)
        return (
            <div id="loading-animation" className="flex flex-col h-[100vh] w-[100vw] items-center justify-center">
                <svg className="rounded-full" viewBox="0 0 800 800" width="200" height="200" xmlns="http://www.w3.org/2000/svg" version="1.1">
                    <defs>
                        <path id="la-wave-1" d="M0 620L21.5 607C43 594 86 568 128.8 557.5C171.7 547 214.3 552 257.2 565.3C300 578.7 343 600.3 385.8 596.7C428.7 593 471.3 564 514.2 557.2C557 550.3 600 565.7 642.8 563.2C685.7 560.7 728.3 540.3 771.2 530.5C814 520.7 857 521.3 878.5 521.7L900 522L900 901L878.5 901C857 901 814 901 771.2 901C728.3 901 685.7 901 642.8 901C600 901 557 901 514.2 901C471.3 901 428.7 901 385.8 901C343 901 300 901 257.2 901C214.3 901 171.7 901 128.8 901C86 901 43 901 21.5 901L0 901Z" fill="#fa7268"></path>
                        <path id="la-wave-2" d="M0 649L21.5 643.5C43 638 86 627 128.8 624.5C171.7 622 214.3 628 257.2 644.2C300 660.3 343 686.7 385.8 686.3C428.7 686 471.3 659 514.2 652.2C557 645.3 600 658.7 642.8 659.7C685.7 660.7 728.3 649.3 771.2 653.5C814 657.7 857 677.3 878.5 687.2L900 697L900 901L878.5 901C857 901 814 901 771.2 901C728.3 901 685.7 901 642.8 901C600 901 557 901 514.2 901C471.3 901 428.7 901 385.8 901C343 901 300 901 257.2 901C214.3 901 171.7 901 128.8 901C86 901 43 901 21.5 901L0 901Z" fill="#eb5967"></path>
                        <path id="la-wave-3" d="M0 766L21.5 757.2C43 748.3 86 730.7 128.8 723.5C171.7 716.3 214.3 719.7 257.2 725C300 730.3 343 737.7 385.8 741C428.7 744.3 471.3 743.7 514.2 736.7C557 729.7 600 716.3 642.8 716C685.7 715.7 728.3 728.3 771.2 735.5C814 742.7 857 744.3 878.5 745.2L900 746L900 901L878.5 901C857 901 814 901 771.2 901C728.3 901 685.7 901 642.8 901C600 901 557 901 514.2 901C471.3 901 428.7 901 385.8 901C343 901 300 901 257.2 901C214.3 901 171.7 901 128.8 901C86 901 43 901 21.5 901L0 901Z" fill="#da3f67"></path>
                        <path id="la-wave-1" d="M0 832L21.5 832C43 832 86 832 128.8 823.7C171.7 815.3 214.3 798.7 257.2 800.8C300 803 343 824 385.8 825.5C428.7 827 471.3 809 514.2 804.5C557 800 600 809 642.8 815.5C685.7 822 728.3 826 771.2 820.2C814 814.3 857 798.7 878.5 790.8L900 783L900 901L878.5 901C857 901 814 901 771.2 901C728.3 901 685.7 901 642.8 901C600 901 557 901 514.2 901C471.3 901 428.7 901 385.8 901C343 901 300 901 257.2 901C214.3 901 171.7 901 128.8 901C86 901 43 901 21.5 901L0 901Z" fill="#c62368"></path>
                        <image id="la-ship" xlinkHref={ArmadaLogoGreen} width="100%" height="100%"/>
                    </defs>
                    <g className="la-parallax">
                        <use xlinkHref="#la-ship" x="0" y="0"/>
                        <use xlinkHref="#la-wave-1"/>
                        <use xlinkHref="#la-wave-2"/>
                        <use xlinkHref="#la-wave-3"/>
                        <use xlinkHref="#la-wave-4"/>
                    </g>
                </svg>
                <p className="font-medium pt-5">Loading...</p>
            </div>
        )
    return <RouterProvider router={router} />
}

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <Provider store={store}>
            <IndexMainLogicWrapper />
        </Provider>
    </React.StrictMode>
)
