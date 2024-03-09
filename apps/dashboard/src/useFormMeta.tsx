import { FORMS } from "@/forms"
import { Form } from "@/forms/form_types"
import { useNavigate, useParams } from "@tanstack/react-router"

/**
 * Given url params this hook can get the form and form page
 * meta information
 */
export function useFormMeta() {
    const navigate = useNavigate()
    const { companyId, formKey, formPageKey } = useParams({
        from: "/$companyId/form/$formKey/$formPageKey"
    })

    if (companyId == null || formKey == null) {
        console.error(
            'Cannot use useFormMeta hook outside of "/$company/$formKey" route'
        )
    }

    const form = (FORMS[formKey as keyof typeof FORMS] ?? null) as Form | null

    // If the formPage is unrecognized, we will default to the first page
    const formPageIndex = Math.max(
        0,
        form?.pages.findIndex(x => x.id === formPageKey) ?? 0
    )

    const formPage =
        formPageIndex < 0 ? null : form?.pages[formPageIndex] ?? null

    if (form == null || formPage == null) {
        navigate({
            from: "/$companyId/form/$formKey/$formPageKey",
            to: "/$companyId/form/$formKey/$formPageKey",
            params: { companyId, formKey, formPageKey: form?.pages[0].id },
            replace: true
        })
    }

    return {
        params: { companyId, formKey, formPageKey: formPageKey },
        form,
        formPage,
        formPageIndex
    }
}
