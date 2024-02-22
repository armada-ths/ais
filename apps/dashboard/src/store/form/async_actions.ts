import { createAsyncThunk } from "@reduxjs/toolkit"
import { HOST } from "../../shared/vars"
import { mapToApi } from "../../utils/mapper"
import { selectSelectedProducts } from "../products/products_selectors"
import { generateProductApiSetArray } from "../products/products_slice"
import { RootState } from "../store"
import { selectForms } from "./form_selectors"
import { FormState, flatMapErrors, setErrors } from "./form_slice"

// First, create the thunk
export const remoteSaveChanges = createAsyncThunk(
    "form/saveChanges",
    async (_, thunkAPI) => {
        thunkAPI.dispatch(setErrors([]))
        const state = thunkAPI.getState() as RootState
        const outgoing = mapToApi(selectForms(state))
        const selectedProducts = selectSelectedProducts(state)

        outgoing.orders = generateProductApiSetArray(selectedProducts)

        const response = await fetch(`${HOST}/api/dashboard/`, {
            method: "PUT",
            body: JSON.stringify(outgoing)
        })
        if (response.status === 400) {
            const errors = await response.json()
            const output: FormState["errors"] = []
            flatMapErrors(output, errors, "")
            thunkAPI.dispatch(setErrors(output))
            return { success: false }
        } else if (response.status !== 200) {
            return { success: false }
        }

        return { success: true }
    }
)
