import { useSelector } from "react-redux"
import { selectForm } from "../../../store/form/form_selectors"
import { PageCard } from "./PageCard"

export function FormSidebarProgressionSummary() {
    const form = useSelector(selectForm)
    return (
        <div className="flex flex-col gap-y-2 bg-slate-200 p-5">
            {form.pages.map(page => (
                <PageCard key={page.id} page={page} />
            ))}
        </div>
    )
}
