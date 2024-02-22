import { PayloadAction, createSlice } from "@reduxjs/toolkit"

export type RegistrationStatus =
    | "before_initial_registration" // Before IR period, and no contract exists
    | "initial_registration"
    | "initial_registration_signed"
    | "after_initial_registration"
    | "after_initial_registration_signed" // The time period between initial registration and complete registration
    | "after_initial_registration_acceptance_accepted" // Past the "acceptance date", if company not marked as accepted, it is rejected
    | "after_initial_registration_acceptance_rejected" // Past the "acceptance date", is rejected
    | "before_complete_registration_ir_unsigned"
    | "before_complete_registration_ir_signed"
    | "complete_registration_ir_unsigned"
    | "complete_registration_ir_signed"
    | "complete_registration_signed"
    | "after_complete_registration"
    | "after_complete_registration_signed"

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
    }
    contract?: {
        name: string
        contract: string
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
            state,
            action: PayloadAction<RegistrationStatus>
        ) => {
            state.status = action.payload
        },
        setUser: (state, action: PayloadAction<CompanyState["user"]>) => {
            state.user = action.payload
        },
        setContract: (
            state,
            action: PayloadAction<CompanyState["contract"]>
        ) => {
            state.contract = action.payload
        }
    }
})

// Action creators are generated for each case reducer function
export const {
    setCompanyRegistrationStatus,
    setUser,
    setCompanyName,
    setContract
} = companySlice.actions

export default companySlice.reducer
