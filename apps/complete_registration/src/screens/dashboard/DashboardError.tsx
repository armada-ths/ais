import { useSelector } from "react-redux"
import { selectErrors } from "../../store/form/form_selectors"

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
            You have not completed Initial Registraion please contact sales at{" "}
            <span className="underline">sales@armada.nu</span>
        </p>
    ),
    user_is_not_exhibitor: (
        <p>
            You did not get picked for the fair this year, contact
            sales@armada.nu if you have any questions
        </p>
    ),
    user_has_no_company: <p>You are not associated with any company</p>
}

export function DashboardError() {
    const error = useSelector(selectErrors)

    if (typeof error !== "string") return null

    return (
        <div className="flex h-[100vh] w-[100vw] flex-col items-center justify-center">
            <p className="mb-4 text-4xl">Oups, something went wrong</p>
            <div className="max-w-xl text-center">{ERRORS[error]}</div>
        </div>
    )
}
