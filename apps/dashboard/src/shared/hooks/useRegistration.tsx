import { HOST } from "@/shared/vars"
import { RegistrationStatus } from "@/store/company/company_slice"
import { useQuery } from "@tanstack/react-query"

export interface RegistrationResponse {
    type: RegistrationStatus
    deadline: string
    has_signed_ir: boolean
    fair: RegistrationFair
    ir_contract: Contract
    cr_contract: unknown
    orders: unknown[]
    contact: Contact
    exhibitor: unknown
    company: Company
}

export interface RegistrationFair {
    name: string
    year: number
    description: string
}

export interface Contract {
    name: string
    contract: string
}

export interface Contact {
    first_name: string
    last_name: string
    email_address: string
    alternative_email_address: unknown
    title: unknown
    mobile_phone_number: unknown
    work_phone_number: unknown
    preferred_language: unknown
}

export interface Company {
    name: string
    identity_number: unknown
    website: unknown
    general_email_address: unknown
    invoice_name: unknown
    invoice_address_line_1: unknown
    invoice_address_line_2: unknown
    invoice_address_line_3: unknown
    invoice_city: unknown
    invoice_zip_code: unknown
    invoice_country: string
    invoice_reference: unknown
    invoice_email_address: unknown
    e_invoice: boolean
    id: number
}

export function useRegistration() {
    return useQuery({
        queryKey: ["registration"],
        queryFn: async () => {
            const response = await fetch(`${HOST}/api/registration`)
            return (await response.json()) as RegistrationResponse
        }
    })
}
