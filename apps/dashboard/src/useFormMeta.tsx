import { FORMS } from "@/forms"
import { Form } from "@/forms/form_types"
import { useNavigate, useParams } from "@tanstack/react-router"

/**
 * Given url params this hook can get the form and form page
 * meta information
 */
export function useFormMeta() {
    const navigate = useNavigate()
    const { companyId, formKey, formStepKey } = useParams({
        from: "/$companyId/form/$formKey/$formStepKey"
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
        form?.pages.findIndex(x => x.id === formStepKey) ?? 0
    )

    const formPage =
        formPageIndex < 0 ? null : form?.pages[formPageIndex] ?? null

    if (form == null || formPage == null) {
        navigate({
            from: "/$companyId/form/$formKey/$formStepKey",
            to: "/$companyId/form/$formKey/$formStepKey",
            params: { companyId, formKey, formStepKey: form?.pages[0].id },
            replace: true
        })
    }

    return {
        params: { companyId, formKey, formPageKey: formStepKey },
        form,
        formPage,
        formPageIndex
    }
}
