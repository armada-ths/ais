import { createAsyncThunk } from "@reduxjs/toolkit"
import { mapToApi } from "../../utils/mapper"
import { RootState } from "../store"
import { generateProductApiSetArray } from "../products/products_slice"
import { selectSelectedProducts } from "../products/products_selectors"
import { selectForms } from "./form_selectors"

// First, create the thunk
export const remoteSaveChanges = createAsyncThunk(
    "form/saveChanges",
    async (_, thunkAPI) => {
        const state = thunkAPI.getState() as RootState
        const outgoing = mapToApi(selectForms(state))
        const selectedProducts = selectSelectedProducts(state)

        outgoing.orders = generateProductApiSetArray(selectedProducts)
        console.log("OUTGOING", JSON.stringify(outgoing))

        const response = await fetch(
            "http://192.168.157.172:3000/api/registration/",
            {
                method: "PUT",
                body: JSON.stringify(outgoing)
            }
        )
        console.log(response)
        return
    }
)
