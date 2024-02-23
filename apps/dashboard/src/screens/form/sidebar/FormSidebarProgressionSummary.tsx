import { useSelector } from "react-redux"
import {
    selectActiveForm,
    selectActivePage
} from "../../../store/form/form_selectors"
import { PageCard } from "./PageCard"

export function FormSidebarProgressionSummary() {
    const form = useSelector(selectActiveForm)
    const activePage = useSelector(selectActivePage)
    return (
        <div className="relative max-h-full">
            <div className="sticky top-0 flex max-h-full flex-col gap-y-2 p-5">
                <h2 className="mb-2 text-center text-xl">Progression</h2>
                {form?.pages.map(page => (
                    <PageCard
                        key={page.id}
                        selected={activePage?.id === page.id}
                        form={form}
                        page={page}
                    />
                ))}
            </div>
        </div>
    )
}
