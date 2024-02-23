import { Button } from "@/components/ui/button"
import { useDispatch } from "react-redux"
import { Form, FormPage } from "../../forms/form_types"
import { remoteSaveChanges } from "../../store/form/async_actions"
import {
    getPageComponent,
    nextPage,
    previousPage
} from "../../store/form/form_slice"
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
    const dispatch = useDispatch<AppDispatch>()

    const Page = getPageComponent(form.key, page.id)

    async function saveChanges() {
        const response = await dispatch(remoteSaveChanges())
        return (response.payload as { success: boolean }).success
    }

    async function handlePrevious() {
        if (await saveChanges()) dispatch(previousPage())
    }

    async function handleNext() {
        if (await saveChanges()) dispatch(nextPage())
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
