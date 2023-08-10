import { createAsyncThunk } from "@reduxjs/toolkit"
import { mapToApi } from "../../utils/mapper"
import { selectForm } from "./form_selectors"
import { RootState } from "../store"
import { generateProductApiSetArray } from "../products/products_slice"
import { useSelector } from "react-redux"
import { selectSelectedProducts } from "../products/products_selectors"

// First, create the thunk
export const remoteSaveChanges = createAsyncThunk(
    "form/saveChanges",
    async (_, thunkAPI) => {
        const state = thunkAPI.getState() as RootState
        const outgoing = mapToApi(selectForm(state))
        const selectedProducts = useSelector(selectSelectedProducts)
        outgoing.products = generateProductApiSetArray(selectedProducts)
        console.log(JSON.stringify(outgoing))

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
