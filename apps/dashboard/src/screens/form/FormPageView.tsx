import { FORMS } from "@/forms"
import { FormPage } from "@/forms/form_types"
import { alertStore } from "@/shared/ConfirmSaveAlert"
import { Provider } from "jotai"

function getPageComponent(formId: keyof typeof FORMS, pageId: string) {
    const form = FORMS[formId]
    if (form == null) return null
    const page = form.pages.find(page => page.id === pageId)
    if (page == null) return null
    return page.pageComponent
}

export function FormPageView({
    formId,
    page
}: {
    formId: keyof typeof FORMS
    page: FormPage
}) {
    const Page = getPageComponent(formId, page.id)

    return (
        <Provider store={alertStore}>
            <div className="mb-10 flex w-full flex-col items-center px-10">
                <h2 className="mb-5 text-2xl">{page.title}</h2>
                <div className="mb-5 flex flex-wrap justify-center gap-x-5">
                    {Page != null && <Page />}
                </div>
            </div>
        </Provider>
    )
}
