import { FormPage } from "./screen"
import { Button } from "primereact/button"
import { useDispatch } from "react-redux"
import { nextPage, previousPage } from "../../store/form/form_slice"
import { AppDispatch } from "../../store/store"
import { remoteSaveChanges } from "../../store/form/async_actions"

export function FormPageView({ page }: { page: FormPage }) {
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
        <div>
            <h2>{page.title}</h2>
            {page.fields.map(field => (
                <div key={field.mapping} className="my-8">
                    {field.component}
                </div>
            ))}
            <div className="flex justify-between gap-x-5">
                <Button label="Previous" onClick={handlePrevious} />
                <Button label="Next" onClick={handleNext} />
            </div>
        </div>
    )
}
