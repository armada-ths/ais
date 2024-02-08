import { useSelector } from "react-redux"
import { selectErrors } from "../../store/form/form_selectors"
import { PrimaryFormHeader } from "../../forms/primary/Header"
import { LogoutButton } from "../../shared/LogoutButton"

const ERRORS = {
    not_authorized: (
        <p>
            You are not logged in, you can{" "}
            <a className="text-emerald-400 underline" href="/register">
                sign in here
            </a>
        </p>
    ),
    user_did_not_sign_ir: (
        <p>
            You have not completed Initial Registration.
        </p>
    ),
    user_is_not_exhibitor: (
        <p>
            You did not get picked for the fair this year.
        </p>
    ),
    user_has_no_company: <p>You are not associated with any company</p>,
    cr_not_open: <p>We are working on this years final registration page, please come back later!</p>
}

export function DashboardError() {
    const error = useSelector(selectErrors)

    if (typeof error !== "string") return null

    return (
        <div className="flex h-[100vh] w-[100vw] flex-col items-center justify-center">
            <div className="max-w-xl text-center mb-10">{ERRORS[error]}</div>
            <PrimaryFormHeader />
            <LogoutButton />
        </div>
    )
}
