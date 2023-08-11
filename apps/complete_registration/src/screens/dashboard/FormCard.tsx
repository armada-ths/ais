import { Card } from "../form/sidebar/PageCard"
import { FORMS } from "../../forms"
import { useDispatch, useSelector } from "react-redux"
import { selectFormProgress } from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { setActiveForm } from "../../store/form/form_slice"

export default function FormCard({
    form
}: {
    form: (typeof FORMS)[keyof typeof FORMS]
}) {
    const dispatch = useDispatch()
    const formProgress = useSelector((state: RootState) =>
        selectFormProgress(state, form.key)
    )

    function openForm() {
        dispatch(setActiveForm(form.key))
    }

    return (
        <Card
            onClick={openForm}
            key={form.key}
            className="max-w-sm p-5 px-8 text-slate-700 transition-all hover:cursor-pointer active:scale-95"
        >
            <div className="mb-2 flex items-center justify-between gap-x-10">
                <p className="text-lg">{form.name}</p>
                {formProgress < 1 ? (
                    <p className="text-yellow-400">{formProgress}%</p>
                ) : (
                    <span className="pi pi-check-circle !font-bold text-emerald-400"></span>
                )}
            </div>
            <p className="text-slate-500">{form.description}</p>
        </Card>
    )
}
