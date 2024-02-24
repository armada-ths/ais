import { useNavigate, useParams } from "@tanstack/react-router"
import { Button } from "primereact/button"
import { Toast } from "primereact/toast"
import { useRef } from "react"
import { useDispatch } from "react-redux"
import { remoteSaveChanges } from "../store/form/async_actions"
import { setActiveForm } from "../store/form/form_slice"
import { AppDispatch } from "../store/store"

export function CompleteButton({
    text,
    save = true
}: {
    text?: string
    save?: boolean
}) {
    const { companyId } = useParams()
    const dispatch = useDispatch<AppDispatch>()
    const navigate = useNavigate()
    const toastRef = useRef<Toast>(null)
    async function complete() {
        let success = true
        if (save) {
            const status = await dispatch(remoteSaveChanges())
            success = (status.payload as { success: boolean }).success
        }
        if (success) {
            dispatch(setActiveForm(null))
            navigate({
                to: "/$companyId",
                params: { companyId }
            })
        } else {
            toastRef.current?.show({
                severity: "error",
                summary: "Error",
                detail: "Failed to save changes, contact sales if error persists"
            })
        }
    }
    return (
        <>
            <Toast ref={toastRef} />
            <Button
                icon="pi pi-check"
                label={text ?? "Complete"}
                onClick={complete}
            />
        </>
    )
}
