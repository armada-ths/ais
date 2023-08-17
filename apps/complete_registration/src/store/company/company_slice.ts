import { createSlice } from "@reduxjs/toolkit"
import { PayloadAction } from "@reduxjs/toolkit"

export type RegistrationStatus =
    | "before_complete_registration" // We are in FR, but no contract uploaded
    | "complete_registration"
    | "complete_registration_signed"

export type CompanyState = {
    status?: RegistrationStatus
    companyName?: string
    user?: {
        first_name: string
        last_name: string
        email_address: string
        alternative_email_address: string | null
        title: string | null
        mobile_phone_number: string | null
        work_phone_number: string | null
        preferred_language: string | null
    },
    contract?: {
        name: string,
        contract: string,
    }
}

const initialState: CompanyState = {}

export const companySlice = createSlice({
    name: "company",
    initialState,
    reducers: {
        setCompanyName: (state, action: PayloadAction<string>) => {
            state.companyName = action.payload
        },
        setCompanyRegistrationStatus: (
            status,
            action: PayloadAction<RegistrationStatus>
        ) => {
            status.status = action.payload
        },
        setUser: (state, action: PayloadAction<CompanyState["user"]>) => {
            state.user = action.payload
        },
        setContract: (state, action: PayloadAction<CompanyState["contract"]>) => {
            state.contract = action.payload
        }
    }
})

// Action creators are generated for each case reducer function
export const { setCompanyRegistrationStatus, setUser, setCompanyName, setContract } =
    companySlice.actions

export default companySlice.reducer
