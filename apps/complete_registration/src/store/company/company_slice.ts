import { createSlice } from "@reduxjs/toolkit"
import { PayloadAction } from "@reduxjs/toolkit"

export type RegistrationStatus =
    | "complete_registration"
    | "complete_registration_signed"

export type CompanyState = {
    status?: RegistrationStatus
}

const initialState: CompanyState = {}

export const companySlice = createSlice({
    name: "company",
    initialState,
    reducers: {
        setCompanyRegistrationStatus: (
            status,
            action: PayloadAction<RegistrationStatus>
        ) => {
            status.status = action.payload
        }
    }
})

// Action creators are generated for each case reducer function
export const { setCompanyRegistrationStatus } = companySlice.actions

export default companySlice.reducer
