import { useFormMeta } from "@/useFormMeta"
import { PageCard } from "./PageCard"

export function FormSidebarProgressionSummary() {
    const { form, formPage } = useFormMeta()

    console.log(formPage?.id)

    return (
        <div className="relative max-h-full">
            <div className="sticky top-0 flex max-h-full flex-col gap-y-2 p-5">
                <h2 className="mb-2 text-center text-xl">Progression</h2>
                {form?.pages.map(page => (
                    <PageCard
                        key={page.id}
                        selected={formPage?.id === page.id}
                        form={form}
                        page={page}
                    />
                ))}
            </div>
        </div>
    )
}
