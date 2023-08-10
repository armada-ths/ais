import { FormPage } from "./screen"
import { Button } from "primereact/button"
import { useDispatch, useSelector } from "react-redux"
import { nextPage, previousPage } from "../../store/form/form_slice"
import { AppDispatch } from "../../store/store"
import { remoteSaveChanges } from "../../store/form/async_actions"
import { FORMS } from "../../forms"
import { selectFormState } from "../../store/form/form_selectors"

export function FormPageView({
    page,
    pageIndex
}: {
    page: FormPage
    pageIndex: number
}) {
    const dispatch = useDispatch<AppDispatch>()

    const formState = useSelector(selectFormState)

    const formWrapper = FORMS[formState.form.key as keyof typeof FORMS]
    const Page = formWrapper.pages[formState.activePage].page

    async function saveChanges() {
        await dispatch(remoteSaveChanges())
    }

    async function handlePrevious() {
        await saveChanges()
        dispatch(previousPage())
    }

    async function handleNext() {
        await saveChanges()
        dispatch(nextPage())
    }

    return (
        <div className="mb-10 flex w-full flex-col items-center px-10">
            <h2 className="text-2xl">{page.title}</h2>
            <div className="mb-5 flex flex-wrap justify-center gap-x-5">
                <Page />
            </div>
            {(page.hasNextButton !== false || page.hasPrevButton !== false) && (
                <div className="flex w-full justify-between gap-x-5">
                    {pageIndex <= 0 && page.hasPrevButton !== false ? (
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
