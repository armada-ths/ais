import { Card } from "../form/sidebar/PageCard"
import { FORMS } from "../../forms"
import { useDispatch, useSelector } from "react-redux"
import { selectFormProgress } from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { setActiveForm } from "../../store/form/form_slice"
import { cx } from "../../utils/cx"

export default function FormCard({
    form,
    locked
}: {
    form: (typeof FORMS)[keyof typeof FORMS]
    locked?: boolean
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
            onClick={locked ? () => {} : openForm}
            key={form.key}
            className={cx(
                "p-5 px-8 text-slate-700 transition-all hover:cursor-pointer active:scale-95",
                locked && "opacity-50 hover:cursor-default active:scale-100"
            )}
        >
            <div className="mb-2 flex items-center justify-between gap-x-10">
                <p className="text-lg">{form.name}</p>
                {formProgress < 1 ? (
                    <p className="text-yellow-400">
                        {(formProgress * 100).toFixed()}%
                    </p>
                ) : (
                    <span className="pi pi-check-circle !font-bold text-emerald-400"></span>
                )}
            </div>
            <p className="text-xs text-slate-500">{form.description}</p>
            <div className="flex-1" />
            {form.key === "primary" && !locked && (
                <p className="mt-2 rounded bg-yellow-500 p-1 px-3 text-white">
                    Contract has not been signed
                </p>
            )}
        </Card>
    )
}
