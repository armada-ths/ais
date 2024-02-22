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
    alternative_email_address: string
    title: string
    mobile_phone_number: string
    work_phone_number: string
    preferred_language: string
}

export interface Company {
    name: string
    identity_number: string
    website: string
    general_email_address: string
    invoice_name: string
    invoice_address_line_1: string
    invoice_address_line_2: string
    invoice_address_line_3: string
    invoice_city: string
    invoice_zip_code: string
    invoice_country: string
    invoice_reference: string
    invoice_email_address: string
    e_invoice: boolean
    id: number
}

export async function queryRegistration() {
    const response = await fetch(`${HOST}/api/registration`)
    const result = (await response.json()) as RegistrationResponse
    return result
}

export function useRegistration() {
    return useQuery({
        queryKey: ["registration"],
        queryFn: queryRegistration
    })
}
