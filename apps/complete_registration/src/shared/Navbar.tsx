import { useDispatch, useSelector } from "react-redux"
import { selectActiveForm } from "../store/form/form_selectors"
import { setActiveForm } from "../store/form/form_slice"
import { AppDispatch } from "../store/store"
import { remoteSaveChanges } from "../store/form/async_actions"
import { useNavigate } from "@tanstack/react-router"

export function Navbar() {
    const dispatch = useDispatch<AppDispatch>()
    const navigate = useNavigate()
    const form = useSelector(selectActiveForm)

    function closeForm() {
        dispatch(setActiveForm(null))
        dispatch(remoteSaveChanges())
        navigate({
            to: "/"
        })
    }

    return (
        <div className="grid grid-cols-[1fr_3fr_1fr] items-center justify-center border-b-2 p-2">
            <div
                className="flex items-center justify-center gap-x-2 hover:cursor-pointer"
                onClick={closeForm}
            >
                <span className="pi pi-arrow-left" />
                <p className="underline">Return back to dashboard</p>
            </div>
            <div className="flex justify-center">
                <h1 className="text-4xl text-slate-700">{form?.name}</h1>
            </div>
        </div>
    )
}
