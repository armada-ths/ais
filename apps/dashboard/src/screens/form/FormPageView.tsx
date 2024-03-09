import { Form, FormPage } from "../../forms/form_types"
import { getPageComponent } from "../../store/form/form_slice"

export function FormPageView({ form, page }: { form: Form; page: FormPage }) {
    const Page = getPageComponent(form.key, page.id)

    return (
        <div className="mb-10 flex w-full flex-col items-center px-10">
            <h2 className="mb-5 text-2xl">{page.title}</h2>
            <div className="mb-5 flex flex-wrap justify-center gap-x-5">
                {Page != null && <Page />}
            </div>
        </div>
    )
}
