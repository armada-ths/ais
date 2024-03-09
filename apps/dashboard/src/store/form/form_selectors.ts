import { createSelector as cs } from "reselect"
import { FORMS, getFieldFromForm } from "../../forms"
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
    () => {
        console.warn("[selectFormPageProgress] is deprecated")
        return 0
    }
)

export const selectFormProgress = cs(
    [
        (state: RootState) => state,
        selectForms,
        (_: RootState, formKey: keyof typeof FORMS) => formKey
    ],
    () => {
        console.warn("[selectFormProgress] is deprecated")
        return 0
    }
)

export const selectCompanyProgress = cs(
    [(state: RootState) => state, selectForms, selectCompanyStatus],
    () => {
        console.warn("[selectCompanyProgress] is deprecated")
        return 0
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
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
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
