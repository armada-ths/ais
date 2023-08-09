import { createSelector as cs } from "reselect"
import { RootState } from "../store"

export const selectFormState = (state: RootState) => state.formMeta
export const selectForm = cs(selectFormState, formMeta => formMeta.form)
export const selectActivePageIndex = cs(
    selectFormState,
    form => form.activePage
)
export const selectActivePage = cs(
    selectForm,
    selectActivePageIndex,
    (form, activePage) => form.pages[activePage]
)

export const selectFormProgress = cs(selectForm, form => {
    const [completedFields, totalFields] = form.pages.reduce(
        (acc, page) => [
            acc[0] +
                page.fields.filter(
                    field => field.type != "text" && field.value != null
                ).length,
            acc[1] + page.fields.filter(field => field.type != "text").length
        ],
        [0, 0]
    )
    return completedFields / totalFields
})
