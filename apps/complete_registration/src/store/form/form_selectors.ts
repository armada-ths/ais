import { createSelector as cs } from "reselect"
import { RootState } from "../store"
import { FORMS } from "../../forms"

export const selectFormState = (state: RootState) => state.formMeta
export const selectForms = cs(selectFormState, formMeta => formMeta.forms)
export const selectForm = cs(
    selectForms,
    (_: RootState, formKey: keyof typeof FORMS) => formKey,
    (forms, formKey) => forms[formKey]
)
export const selectActiveForm = cs(selectFormState, formState =>
    formState.activeForm == null ? null : formState.forms[formState.activeForm]
)
export const selectActivePageIndex = cs(
    selectFormState,
    formState => formState.activePage
)
export const selectActivePage = cs(
    selectActiveForm,
    selectActivePageIndex,
    (activeForm, activePage) => activeForm?.pages[activePage]
)

export const selectPageProgress = cs(
    [selectActiveForm, (_: RootState, pageId: string) => pageId],
    (form, pageId) => {
        if (form == null) return null
        const page = form.pages.find(p => p.id == pageId)
        if (page == null) return null
        const totalFields =
            page.fields?.filter(
                field => field.includeInProgressionSummary !== false
            ).length ?? 0
        const completedFields =
            page.fields?.filter(
                field =>
                    field.value && field.includeInProgressionSummary !== false
            ).length ?? 0

        if (totalFields <= 0) return null
        return completedFields / totalFields
    }
)

export const selectFormProgress = cs(
    [selectForms, (_: RootState, formKey: keyof typeof FORMS) => formKey],
    (forms, formKey) => {
        const form = forms[formKey]

        const [completedFields, totalFields] = form.pages.reduce(
            (acc, page) => [
                acc[0] +
                    (page.fields?.filter(
                        field =>
                            field.value &&
                            field.includeInProgressionSummary !== false
                    ).length ?? 0),
                acc[1] +
                    (page.fields?.filter(
                        field => field.includeInProgressionSummary !== false
                    ).length ?? 0)
            ],
            [0, 0]
        )
        return completedFields / (totalFields || 1)
    }
)

export const selectField = cs(
    [selectForms, (_: RootState, mapping: string) => mapping],
    (forms, mapping) => {
        // Iterate over all forms and pages to find the field with the given mapping
        for (const formMeta of Object.values(forms)) {
            for (const page of formMeta.pages) {
                const field = page.fields?.find(f => f.mapping == mapping) ?? 0
                if (field) return field
            }
        }
        return null
    }
)
