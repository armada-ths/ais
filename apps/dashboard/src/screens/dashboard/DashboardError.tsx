import { useSelector } from "react-redux"
import { PrimaryFormHeader } from "../../forms/Header"
import { LogoutButton } from "../../shared/LogoutButton"
import { selectErrors } from "../../store/form/form_selectors"

const ERRORS = {
    not_authorized: (
        <p>
            You are not logged in, you can{" "}
            <a className="text-emerald-400 underline" href="/dashboard">
                sign in here
            </a>
        </p>
    ),
    user_did_not_sign_ir: <p>You have not completed Initial Registration.</p>,
    user_is_not_exhibitor: (
        <p>
            Unfortunetly we are at full captity as of right now, we might get
            space for more exhibitors later and will contact you then.
        </p>
    ),
    user_has_no_company: <p>You are not associated with any company</p>,
    cr_not_open: (
        <p>
            We are working on this years final registration page, please come
            back later!
        </p>
    )
}

export function DashboardError() {
    const error = useSelector(selectErrors)

    if (typeof error !== "string") return null

    return (
        <div className="flex h-[100vh] w-[100vw] flex-col items-center justify-center">
            <LogoutButton />
            <p className="mb-4 text-4xl">Oups, something went wrong</p>
            <div className="mb-10 max-w-xl text-center">{ERRORS[error]}</div>
            <PrimaryFormHeader />
        </div>
    )
}
