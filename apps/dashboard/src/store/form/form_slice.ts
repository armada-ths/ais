import { createSlice } from "@reduxjs/toolkit"
import { FORMS, getMutableFormsInstance } from "../../forms"
import { PayloadAction } from "@reduxjs/toolkit"
import { FieldValue } from "../../forms/form_types"

export function getPageComponent(formId: keyof typeof FORMS, pageId: string) {
    const form = FORMS[formId]
    if (form == null) return null
    const page = form.pages.find(page => page.id === pageId)
    if (page == null) return null
    return page.pageComponent
}

export function flatMapErrors(
    output: NonNullable<FormState["errors"]>,
    errors: unknown,
    currentMapping: string
) {
    if (errors == null) return
    if (Array.isArray(errors)) {
        let i = 0
        for (const error of errors) {
            flatMapErrors(output, error, `${currentMapping}.$${i}`)
            i++
        }
    } else if (typeof errors === "object") {
        for (const [key, value] of Object.entries(errors)) {
            flatMapErrors(output, value, `${currentMapping}.${key}`)
        }
    } else {
        output.push({
            mapping: currentMapping.slice(1),
            error: errors.toString()
        })
    }
}

// Create a recursive type with objects, strings, numbers and booleans
export type FormState = {
    activePage: number
    activeForm?: keyof typeof FORMS
    forms: typeof FORMS
    errors?: {
        mapping: string
        error: string
    }[]
}

const initialState: FormState = {
    activePage: 0,
    forms: getMutableFormsInstance()
}

export const formSlice = createSlice({
    name: "formMeta",
    initialState,
    reducers: {
        reset: () => initialState,
        setActiveForm: (
            state,
            action: PayloadAction<keyof typeof FORMS | null>
        ) => {
            if (action.payload == null) state.activePage = 0

            state.activeForm = action.payload ?? undefined
        },
        setErrors: (state, action: PayloadAction<FormState["errors"]>) => {
            state.errors = action.payload
        },
        setPage: (state, action: PayloadAction<string | number>) => {
            if (state.activeForm == null) return
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
            if (state.activeForm == null) return
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
            for (const form of Object.values(state.forms)) {
                // Const find a specific field in state
                for (const page of form.pages) {
                    const result = page.fields?.find(
                        field => field.mapping === action.payload.mapping
                    )
                    if (result == null) continue
                    result.value = action.payload.value
                    return
                }
            }
        }
    }
})

// Action creators are generated for each case reducer function
export const {
    setErrors,
    setActiveForm,
    setPage,
    nextPage,
    previousPage,
    setField
} = formSlice.actions

export default formSlice.reducer
