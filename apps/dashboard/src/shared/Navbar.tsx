import { useFormMeta } from "@/useFormMeta"
import { useNavigate } from "@tanstack/react-router"
import { useDispatch } from "react-redux"
import { remoteSaveChanges } from "../store/form/async_actions"
import { AppDispatch } from "../store/store"

export function Navbar() {
    const dispatch = useDispatch<AppDispatch>()
    const navigate = useNavigate()

    const {
        form,
        params: { companyId }
    } = useFormMeta()

    async function closeForm() {
        await dispatch(remoteSaveChanges())
        navigate({
            to: "/$companyId",
            params: { companyId }
        })
    }

    return (
        <div className="grid h-20 grid-cols-[1fr_3fr] items-center justify-center border-b-2 p-2 md:grid-cols-[1fr_3fr_1fr]">
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
                <h1 className="text-2xl text-slate-700 md:text-4xl">
                    {form?.name}
                </h1>
            </div>
        </div>
    )
}
