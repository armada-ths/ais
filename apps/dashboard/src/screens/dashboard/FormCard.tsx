import { Badge } from "@/components/ui/badge"
import { Form } from "@/forms/form_types"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { cx } from "@/utils/cx"
import { useNavigate } from "@tanstack/react-router"
import { Card } from "../form/sidebar/PageCard"

export default function FormCard({
    form,
    locked
}: {
    form: Form
    locked?: boolean
}) {
    const navigate = useNavigate({
        from: "/$companyId/*"
    })

    const { data: dataRegistration } = useDashboard()
    const { data: dataProducts } = useProducts()

    function openForm() {
        navigate({
            to: `/$companyId/form/$formKey/$formPageKey`,
            params: { formKey: form.key, formPageKey: form.pages[0].id }
        })
    }

    if (dataRegistration == null || dataProducts == null)
        return <p>Could not load necessary data...</p>

    // Go through the form and check which pages can be considered done
    const results = form.pages.map(
        page =>
            page.isDone?.({
                form,
                dashboard: dataRegistration,
                products: dataProducts
            }) ?? null
    )

    // Only compare pages that have a isDone function
    // if an isDone function returns null, it is also ignored
    const progress =
        results.filter(Boolean).length / results.filter(x => x != null).length

    return (
        <Card
            onClick={locked ? () => {} : openForm}
            key={form.key}
            className={cx(
                "max-w-[500px] p-5 px-8 text-slate-700 transition-all hover:cursor-pointer active:scale-95",
                {
                    "opacity-50 hover:cursor-default active:scale-100": locked
                }
            )}
        >
            <div className="mb-2 flex items-center justify-between gap-x-10">
                <p className="text-lg">{form.name}</p>
                {form.progression !== "none" &&
                    (progress <= 0 && !form.forceFormDone ? (
                        <Badge className="whitespace-nowrap">Not Started</Badge>
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
            {form.key === "fr_accounting" && !locked && (
                <p className="mt-4 rounded bg-yellow-500 p-1 px-3 text-white">
                    Order not confirmed
                </p>
            )}
        </Card>
    )
}
