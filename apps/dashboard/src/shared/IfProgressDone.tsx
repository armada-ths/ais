import { FORMS, FormIds, FormPageIds } from "@/forms"
import { FormPage } from "@/forms/form_types"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { useMemo } from "react"

export function IfProgressDone({
    page: pagePath,
    fallback,
    children
}: {
    page: `${FormIds}.${FormPageIds}`
    fallback?: React.ReactNode // What to render if the page is not done
    children?: React.ReactNode
}) {
    const [formId, pageId] = pagePath.split(".") as [FormIds, FormPageIds]

    const { data: dataProducts, isLoading: isLoadingProducts } = useProducts()
    const { data: dataDashboard, isLoading: isLoadingDasboard } = useDashboard()

    // If form is not provided, try to find the form by the pageId
    // This is slower but better DX
    const activeForm = useMemo(() => FORMS[formId], [formId])

    const page = useMemo(
        () => activeForm?.pages.find(page => page.id === pageId),
        [activeForm?.pages, pageId]
    ) as FormPage

    if (activeForm == null || page == null) {
        console.warn("Could not find form or page", activeForm, pageId)
        return fallback
    }

    if (isLoadingProducts || isLoadingDasboard) return null
    if (dataProducts == null || dataDashboard == null) return fallback

    const isDone = page?.isDone?.({
        form: activeForm,
        products: dataProducts,
        registration: dataDashboard
    })

    return isDone ? <>{children}</> : fallback
}
