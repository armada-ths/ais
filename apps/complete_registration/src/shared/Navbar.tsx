import { useDispatch, useSelector } from "react-redux"
import { selectActiveForm } from "../store/form/form_selectors"
import { setActiveForm } from "../store/form/form_slice"

export function Navbar() {
    const dispatch = useDispatch()
    const form = useSelector(selectActiveForm)

    function closeForm() {
        dispatch(setActiveForm(null))
    }

    return (
        <div className="grid h-[8vh] grid-cols-[1fr_3fr_1fr] items-center justify-center border-b-2">
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
