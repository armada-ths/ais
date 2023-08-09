import { createAsyncThunk } from "@reduxjs/toolkit"
import { mapToApi } from "../../utils/mapper"
import { selectForm } from "./form_selectors"
import { RootState } from "../store"

// First, create the thunk
export const remoteSaveChanges = createAsyncThunk(
    "form/saveChanges",
    async (_, thunkAPI) => {
        const state = thunkAPI.getState() as RootState
        const outgoing = mapToApi(selectForm(state))
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
