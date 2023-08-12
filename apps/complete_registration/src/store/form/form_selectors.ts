import { createSelector as cs } from "reselect"
import { RootState } from "../store"
import { FORMS } from "../../forms"
import { Field, FormPage } from "../../screens/form/screen"

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
    [selectForms, (_: RootState, formKey: keyof typeof FORMS) => formKey],
    (forms, formKey) => {
        const form = forms[formKey]

        const [completedFields, totalFields] = form.pages.reduce(
            (acc, page) => [
                acc[0] +
                    (page.fields?.filter(
                        field => field.value && field.mandatory !== false
                    ).length ?? 0),
                acc[1] +
                    (page.fields?.filter(field => field.mandatory !== false)
                        .length ?? 0)
            ],
            [0, 0]
        )
        return completedFields / (totalFields || 1)
    }
)

export const selectCompanyProgress = cs(selectForms, forms => {
    let completedFields = 0
    let totalFields = 0
    for (const form of Object.values(forms)) {
        for (const page of form.pages) {
            for (const field of page.fields ?? []) {
                if (field.mandatory !== false) totalFields++
                if (field.mandatory !== false && field.value) completedFields++
            }
        }
    }
    return completedFields / (totalFields || 1)
})

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
export const selectErrors = cs(selectFormState, formState => formState.errors)
export const selectFieldErrors = cs(
    [selectFormState, (_: RootState, mapping: string) => mapping],
    (formState, mapping) => {
        for (const error of formState.errors ?? []) {
            console.log(
                error.mapping.split(".").slice(0, -1).join("."),
                mapping,
                error.mapping.split(".").slice(0, -1).join(".") === mapping
            )
            if (error.mapping.split(".").slice(0, -1).join(".") === mapping) {
                console.log("FOUND MAP!!!!!!!!!!!", error)
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
        for (const page of selectedForm.pages) {
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
