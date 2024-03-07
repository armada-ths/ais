import { Button } from "@/components/ui/button"
import { useNavigate } from "@tanstack/react-router"
import { useDispatch } from "react-redux"
import { Form, FormPage } from "../../forms/form_types"
import { remoteSaveChanges } from "../../store/form/async_actions"
import { getPageComponent } from "../../store/form/form_slice"
import { AppDispatch } from "../../store/store"

export function FormPageView({
    form,
    page,
    pageIndex
}: {
    form: Form
    page: FormPage
    pageIndex: number
}) {
    const navigate = useNavigate({
        from: "/$companyId/form/$formKey/$formStepKey"
    })
    const dispatch = useDispatch<AppDispatch>()

    const Page = getPageComponent(form.key, page.id)

    async function saveChanges() {
        const response = await dispatch(remoteSaveChanges())
        return (response.payload as { success: boolean }).success
    }

    async function handlePrevious() {
        await saveChanges()
        const previousPage = form.pages[pageIndex - 1]
        navigate({
            to: "/$companyId/form/$formKey/$formStepKey",
            params: { formStepKey: previousPage.id }
        })
    }

    async function handleNext() {
        await saveChanges()
        const nextPage = form.pages[pageIndex + 1]
        navigate({
            to: "/$companyId/form/$formKey/$formStepKey",
            params: { formStepKey: nextPage.id }
        })
    }

    return (
        <div className="mb-10 flex w-full flex-col items-center px-10">
            <h2 className="mb-5 text-2xl">{page.title}</h2>
            <div className="mb-5 flex flex-wrap justify-center gap-x-5">
                {Page != null && <Page />}
            </div>
            {(page.hasNextButton !== false || page.hasPrevButton !== false) && (
                <div className="flex w-full justify-between gap-x-5">
                    {pageIndex <= 0 || page.hasPrevButton === false ? (
                        <div />
                    ) : (
                        <Button onClick={handlePrevious}>Previous</Button>
                    )}
                    {page.hasNextButton !== false && (
                        <Button onClick={handleNext}>Next</Button>
                    )}
                </div>
            )}
        </div>
    )
}
