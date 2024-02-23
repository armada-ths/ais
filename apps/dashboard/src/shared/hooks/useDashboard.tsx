import { HOST } from "@/shared/vars"
import { RegistrationStatus } from "@/store/company/company_slice"
import { useQuery } from "@tanstack/react-query"
import { useNavigate, useParams } from "@tanstack/react-router"

export interface DashboardResponse {
    type: RegistrationStatus
    deadline: string
    has_signed_ir: boolean
    fair: RegistrationFair
    ir_contract: Contract
    cr_contract: Contract
    sales_contacts: SalesContact[]
    orders: unknown[]
    contact: Contact
    exhibitor: unknown
    company: Company
}

export interface SalesContact {
    first_name: string
    last_name: string
    title: string
    email: string
    phone_number: string
    picture_original: string
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

export async function queryDashboard(args?: { companyId?: number }) {
    const response = await fetch(
        `${HOST}/api/dashboard${args?.companyId ? `/${args.companyId}` : ""}`
    )
    const result = (await response.json()) as DashboardResponse
    return result
}

export function useDashboard() {
    const navigation = useNavigate()
    const { companyId: rawCompanyId } = useParams()

    // Check that if company is defined it is a positive number, otherwise set it to -1 to indicate that it is not a valid company
    const companyId =
        rawCompanyId === undefined
            ? undefined
            : isNaN(Number(rawCompanyId))
            ? -1
            : Number(rawCompanyId)

    const args = useQuery({
        queryKey: ["registration", companyId],
        queryFn: async ({ queryKey: [, companyId] }) =>
            queryDashboard({ companyId: companyId as number }),
        enabled: companyId === undefined || companyId > 0
    })

    if (
        (companyId != null && companyId < 0) ||
        (args.data &&
            "error" in args.data &&
            typeof args.data.error === "string" &&
            ["not_authorized", "company_does_not_exist"].includes(
                args.data.error
            ))
    ) {
        navigation({
            to: "/404",
            replace: true
        })
    }

    return args
}
