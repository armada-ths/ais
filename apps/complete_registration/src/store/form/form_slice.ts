import { createSlice } from "@reduxjs/toolkit"
import { FieldValue } from "../../screens/form/screen"
import { FORMS, getMutableFormsInstance } from "../../forms"
import { PayloadAction } from "@reduxjs/toolkit"

export function getPageComponent(formId: keyof typeof FORMS, pageId: string) {
    const form = FORMS[formId]
    if (form == null) return null
    const page = form.pages.find(page => page.id === pageId)
    if (page == null) return null
    return page.pageComponent
}

export type FormState = {
    activePage: number
    activeForm: keyof typeof FORMS
    forms: typeof FORMS
}

const initialState: FormState = {
    activePage: 0,
    activeForm: "primary",
    forms: getMutableFormsInstance()
}

export const formSlice = createSlice({
    name: "formMeta",
    initialState,
    reducers: {
        reset: () => initialState,
        setActiveForm: (state, action: PayloadAction<keyof typeof FORMS>) => {
            state.activeForm = action.payload
        },
        setPage: (state, action: PayloadAction<string | number>) => {
            // Set index
            if (typeof action.payload === "number") {
                state.activePage = action.payload
                return
            }
            const activeForm = state.forms[state.activeForm]
            // Set by page id
            const pageIndex = activeForm.pages.findIndex(
                page => page.id === action.payload
            )
            state.activePage = pageIndex === -1 ? 0 : pageIndex
        },
        nextPage: state => {
            const activeForm = state.forms[state.activeForm]
            if (state.activePage < activeForm.pages.length - 1)
                state.activePage++
        },
        previousPage: state => {
            if (state.activePage > 0) state.activePage--
        },
        setField: (
            state,
            action: PayloadAction<{ mapping: string; value: FieldValue }>
        ) => {
            const activeForm = state.forms[state.activeForm]
            // Const find a specific field in state
            for (const page of activeForm.pages) {
                const result = page.fields?.find(
                    field => field.mapping === action.payload.mapping
                )
                if (result == null) continue
                result.value = action.payload.value
            }
        }
    }
})

// Action creators are generated for each case reducer function
export const { setActiveForm, setPage, nextPage, previousPage, setField } =
    formSlice.actions

export default formSlice.reducer
