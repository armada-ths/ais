import { useNavigate, useParams } from "@tanstack/react-router"
import { Button } from "primereact/button"
import { Toast } from "primereact/toast"
import { useRef } from "react"

export function CompleteButton({ text }: { text?: string }) {
    const { companyId } = useParams({
        from: "/$companyId/*"
    })
    const navigate = useNavigate()
    const toastRef = useRef<Toast>(null)
    async function complete() {
        const success = true
        if (success) {
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
