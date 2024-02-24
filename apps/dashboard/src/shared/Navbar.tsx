import { useNavigate, useParams } from "@tanstack/react-router"
import { useDispatch, useSelector } from "react-redux"
import { remoteSaveChanges } from "../store/form/async_actions"
import { selectActiveForm } from "../store/form/form_selectors"
import { setActiveForm } from "../store/form/form_slice"
import { AppDispatch } from "../store/store"

export function Navbar() {
    const { companyId } = useParams()
    const dispatch = useDispatch<AppDispatch>()
    const navigate = useNavigate()
    const form = useSelector(selectActiveForm)

    function closeForm() {
        dispatch(setActiveForm(null))
        dispatch(remoteSaveChanges())
        navigate({
            to: "/$companyId",
            params: { companyId }
        })
    }

    return (
        <div className="grid h-20 grid-cols-[1fr_3fr_1fr] items-center justify-center border-b-2 p-2">
            <div
                className="ml-8 flex items-center justify-start gap-x-2 hover:cursor-pointer"
                onClick={closeForm}
            >
                <span className="pi pi-arrow-left" />
                <p className="hidden hover:underline lg:block">
                    Return to dashboard
                </p>
            </div>
            <div className="flex justify-center">
                <h1 className="text-4xl text-slate-700">{form?.name}</h1>
            </div>
        </div>
    )
}
