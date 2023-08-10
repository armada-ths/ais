import { createSlice } from "@reduxjs/toolkit"
import { FieldValue, Form } from "../../screens/form/screen"
import { FORMS } from "../../forms"
import { PayloadAction } from "@reduxjs/toolkit"

export type FormState = { activePage: number; form: Form }

const initialState: FormState = {
    activePage: 0,
    form: FORMS.primary
}

export const counterSlice = createSlice({
    name: "formMeta",
    initialState,
    reducers: {
        reset: () => initialState,
        setPage: (state, action: PayloadAction<string>) => {
            const pageIndex = state.form.pages.findIndex(
                page => page.id === action.payload
            )
            state.activePage = pageIndex === -1 ? 0 : pageIndex
        },
        nextPage: state => {
            if (state.activePage < state.form.pages.length - 1)
                state.activePage++
        },
        previousPage: state => {
            if (state.activePage > 0) state.activePage--
        },
        setField: (
            state,
            action: PayloadAction<{ mapping: string; value: FieldValue }>
        ) => {
            // Const find a specific field in state
            for (const page of state.form.pages) {
                const result = page.fields.find(
                    field => field.mapping === action.payload.mapping
                )
                if (result == null) continue
                result.value = action.payload.value
            }
        }
    }
})

// Action creators are generated for each case reducer function
export const { setPage, nextPage, previousPage, setField } =
    counterSlice.actions

export default counterSlice.reducer
