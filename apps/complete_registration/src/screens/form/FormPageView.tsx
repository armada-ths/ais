import { Form, FormPage } from "./screen"
import { Button } from "primereact/button"
import { useDispatch } from "react-redux"
import {
    getPageComponent,
    nextPage,
    previousPage
} from "../../store/form/form_slice"
import { AppDispatch } from "../../store/store"
import { remoteSaveChanges } from "../../store/form/async_actions"

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
                        <Button
                            icon="pi pi-arrow-left"
                            label="Previous"
                            onClick={handlePrevious}
                        />
                    )}
                    {page.hasNextButton !== false && (
                        <Button
                            icon="pi pi-arrow-right"
                            label="Next"
                            iconPos="right"
                            onClick={handleNext}
                        />
                    )}
                </div>
            )}
        </div>
    )
}
