import { Badge } from "@/components/ui/badge"
import { useDashboard } from "@/shared/hooks/useDashboard"
import { useProducts } from "@/shared/hooks/useProducts"
import { useNavigate } from "@tanstack/react-router"
import { useDispatch } from "react-redux"
import { FORMS } from "../../forms"
import { setActiveForm } from "../../store/form/form_slice"
import { cx } from "../../utils/cx"
import { Card } from "../form/sidebar/PageCard"

export default function FormCard({
    form,
    locked
}: {
    form: (typeof FORMS)[keyof typeof FORMS]
    locked?: boolean
}) {
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const { data: dataRegistration } = useDashboard()
    const { data: dataProducts } = useProducts()

    function openForm() {
        dispatch(setActiveForm(form.key))
        navigate({
            to: `/form/${form.key}`
        })
    }

    if (dataRegistration == null || dataProducts == null)
        return <p>Could not load necessary data...</p>

    // Go through the form and check which pages can be considered done
    const results = form.pages.map(
        page =>
            page.isDone?.({
                form,
                registration: dataRegistration,
                products: dataProducts
            }) ?? null
    )

    // Only compare pages that have a isDone function
    const progress =
        results.filter(Boolean).length /
        form.pages.filter(x => x.isDone != null).length

    return (
        <Card
            onClick={locked ? () => {} : openForm}
            key={form.key}
            className={cx(
                "p-5 px-8 text-slate-700 transition-all hover:cursor-pointer active:scale-95",
                {
                    "opacity-50 hover:cursor-default active:scale-100": locked
                }
            )}
        >
            <div className="mb-2 flex items-center justify-between gap-x-10">
                <p className="text-lg">{form.name}</p>
                {form.progression !== "none" &&
                    (progress <= 0 && !form.forceFormDone ? (
                        <Badge>Not Started</Badge>
                    ) : progress < 1 && !form.forceFormDone ? (
                        <p className="text-yellow-400">
                            {(progress * 100).toFixed()}%
                        </p>
                    ) : (
                        <span className="pi pi-check-circle !font-bold text-emerald-400"></span>
                    ))}
            </div>
            <p className="text-xs text-slate-500">{form.description}</p>
            <div className="flex-1" />
            {form.key === "primary" && !locked && (
                <p className="mt-4 rounded bg-yellow-500 p-1 px-3 text-white">
                    Order not confirmed
                </p>
            )}
        </Card>
    )
}