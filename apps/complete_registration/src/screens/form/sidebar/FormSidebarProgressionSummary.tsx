import { useSelector } from "react-redux"
import {
    selectActivePage,
    selectForm
} from "../../../store/form/form_selectors"
import { PageCard } from "./PageCard"

export function FormSidebarProgressionSummary() {
    const form = useSelector(selectForm)
    const activePage = useSelector(selectActivePage)
    return (
        <div className="relative h-[100vh]">
            <div className="sticky top-0 flex max-h-[100vh] flex-col gap-y-2 p-5">
                <h2 className="mb-2 text-center text-xl">Progression</h2>
                {form.pages.map(page => (
                    <PageCard
                        key={page.id}
                        selected={activePage.id === page.id}
                        page={page}
                    />
                ))}
            </div>
        </div>
    )
}
