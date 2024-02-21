import { createSelector as cs } from "reselect"
import { FORMS, getFieldFromForm } from "../../forms"
import { FORM_ACCESS } from "../../forms/form_access"
import { Field, FormPage } from "../../forms/form_types"
import { selectCompanyStatus } from "../company/company_selectors"
import { RootState } from "../store"

export function selectFormState(state: RootState) {
    return state.formMeta
}
export const selectForms = cs(selectFormState, formMeta => formMeta.forms)
export const selectForm = cs(
    selectForms,
    (_: RootState, formKey?: keyof typeof FORMS) => formKey,
    (forms, formKey) => (formKey == null ? null : forms[formKey])
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

export const selectFormPageProgress = cs(
    [
        (state: RootState) => state,
        // If no worm key is provided, the active form will be used
        (state: RootState, _: string, formKey?: keyof typeof FORMS) =>
            formKey == null
                ? selectActiveForm(state)
                : selectForm(state, formKey),
        (_: RootState, pageId: string) => pageId
    ],
    (state, form, pageId) => {
        if (form == null) {
            return null
        }
        const page = form.pages.find(p => p.id == pageId)
        if (page == null) return null
        if (page.getProgress != null) page.getProgress(state)

        const totalFields =
            page.fields?.filter(field => field.mandatory !== false).length ?? 0
        const completedFields =
            page.fields?.filter(
                field => field.value && field.mandatory !== false
            ).length ?? 0

        if (totalFields <= 0) return null
        return completedFields / totalFields
    }
)

export const selectFormProgress = cs(
    [
        (state: RootState) => state,
        selectForms,
        (_: RootState, formKey: keyof typeof FORMS) => formKey
    ],
    (state, forms, formKey) => {
        const form = forms[formKey]
        if (form.progression === "none" || form.progression === "silent")
            return -1

        const pageProgress = form.pages
            .map(page => selectFormPageProgress(state, page.id, form.key))
            .filter(Boolean) as number[]

        return (
            pageProgress.reduce((a, b) => a + b, 0) / (pageProgress.length || 1)
        )
    }
)

export const selectCompanyProgress = cs(
    [(state: RootState) => state, selectForms, selectCompanyStatus],
    (state, forms, companyStatus) => {
        let averageProgress = 0
        let formCount = 0

        // Filter forms that are not relevant
        const listOfSkippedForms = []
        for (const current of Object.values(forms)) {
            if (companyStatus == null) {
                listOfSkippedForms.push(current.key)
                continue
            }
            if (FORM_ACCESS[companyStatus]?.[current.key] === "shown") continue
            listOfSkippedForms.push(current.key)
        }

        for (const form of Object.values(forms)) {
            if (
                form.progression === "none" ||
                form.progression === "silent" ||
                listOfSkippedForms.includes(form.key)
            ) {
                continue
            }
            averageProgress += selectFormProgress(state, form.key)
            formCount++
        }

        return averageProgress / (formCount || 1)
    }
)

export const selectField = cs(
    [selectForms, (_: RootState, mapping: string) => mapping],
    (forms, mapping) => {
        return getFieldFromForm(forms, mapping)
    }
)
export const selectErrors = cs(selectFormState, formState => formState.errors)
export const selectFieldErrors = cs(
    [selectFormState, (_: RootState, mapping: string) => mapping],
    (formState, mapping) => {
        for (const error of formState.errors ?? []) {
            if (error.mapping.split(".").slice(0, -1).join(".") === mapping) {
                return error
            }
        }
        return null
    }
)
export const selectUnfilledFields = cs(
    (state: RootState, formKey: keyof typeof FORMS) =>
        selectForm(state, formKey),
    selectedForm => {
        const unfilledFields: { page: FormPage; fields: Field[] }[] = []
        for (const page of selectedForm?.pages ?? []) {
            const newUnfilledPage: (typeof unfilledFields)[number] = {
                page,
                fields: []
            }
            for (const field of page.fields ?? []) {
                if (!field.value && field.mandatory !== false)
                    newUnfilledPage.fields.push(field)
            }
            if (newUnfilledPage.fields.length == 0) continue
            unfilledFields.push(newUnfilledPage)
        }
        return unfilledFields
    }
)
