import { RootState } from "../store"

export const selectCompanyStatus = (state: RootState) => state.company.status
export const selectUser = (state: RootState) => state.company.user
export const selectCompanyName = (state: RootState) => state.company.companyName
