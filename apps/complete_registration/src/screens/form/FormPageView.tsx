import { FormPage } from "./screen"
import { Button } from "primereact/button"
import { useDispatch } from "react-redux"
import { nextPage, previousPage } from "../../store/form/form_slice"
import { AppDispatch } from "../../store/store"
import { remoteSaveChanges } from "../../store/form/async_actions"

export function FormPageView({
    page,
    pageIndex
}: {
    page: FormPage
    pageIndex: number
}) {
    const dispatch = useDispatch<AppDispatch>()

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
            <div className="flex flex-wrap justify-center gap-x-5">
                {page.fields.map(field => field.component)}
            </div>
            <div className="flex w-full justify-between gap-x-5">
                {pageIndex <= 0 ? (
                    <div />
                ) : (
                    <Button
                        icon="pi pi-arrow-left"
                        label="Previous"
                        onClick={handlePrevious}
                    />
                )}
                <Button
                    icon="pi pi-arrow-right"
                    label="Next"
                    iconPos="right"
                    onClick={handleNext}
                />
            </div>
        </div>
    )
}
