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

export const selectPageProgress = cs(
    [selectForm, (state: RootState, pageId: string) => pageId],
    (form, pageId) => {
        const page = form.pages.find(p => p.id == pageId)
        if (page == null) return null
        const totalFields = page.fields.filter(
            field => field.type != "text"
        ).length
        const completedFields = page.fields.filter(
            field => field.type != "text" && field.value
        ).length

        if (totalFields <= 0) return null
        return completedFields / totalFields
    }
)

export const selectFormProgress = cs(selectForm, form => {
    const [completedFields, totalFields] = form.pages.reduce(
        (acc, page) => [
            acc[0] +
                page.fields.filter(field => field.type != "text" && field.value)
                    .length,
            acc[1] + page.fields.filter(field => field.type != "text").length
        ],
        [0, 0]
    )
    return completedFields / totalFields
})
