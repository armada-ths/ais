import { RootState } from "../store"

export const selectCompanyStatus = (state: RootState) => state.company.status
