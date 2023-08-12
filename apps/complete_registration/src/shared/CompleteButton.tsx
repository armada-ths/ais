import { Button } from "primereact/button"
import { useDispatch } from "react-redux"
import { setActiveForm } from "../store/form/form_slice"
import { remoteSaveChanges } from "../store/form/async_actions"
import { AppDispatch } from "../store/store"

export function CompleteButton({
    text,
    save = true
}: {
    text?: string
    save?: boolean
}) {
    const dispatch = useDispatch<AppDispatch>()
    function complete() {
        dispatch(setActiveForm(null))
        if (save) dispatch(remoteSaveChanges())
    }
    return (
        <Button
            icon="pi pi-check"
            label={text ?? "Complete"}
            onClick={complete}
        />
    )
}
