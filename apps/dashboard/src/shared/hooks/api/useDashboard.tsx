import { HOST } from "@/shared/vars"
import { RegistrationStatus } from "@/store/company/company_slice"
import { QueryClient, useQuery } from "@tanstack/react-query"
import { useNavigate, useParams } from "@tanstack/react-router"

export interface DashboardResponse {
    type: RegistrationStatus
    deadline: string
    has_signed_ir: boolean
    fair: RegistrationFair
    ir_contract: Contract
    cr_contract: Contract
    sales_contacts: SalesContact[]
    orders: Order[]
    contact: Contact | null
    exhibitor: unknown
    company: Company
    products: Product[]
    interested_in: Array<{ id: number }>
}

export interface Order {
    id: number
    comment: string
    quantity: number
    unit_price?: number
    product: Product
}

export interface Category {
    id: number
    name: "Package" | "Additional booth area" | "Non Visible Package"
    description: string
    allow_multiple_purchases: boolean
}

export interface RegistrationSection {
    id: string
    name: string
    description: string
    hide_from_registration: boolean
}

export interface ChildProduct {
    quantity: number
    child_product: Omit<Product, "child_products">
}

export interface Product {
    id: number
    name: string
    short_name: string
    max_quantity: number
    unit_price: number
    description: string
    category: Category | null
    display_in_product_list: boolean
    registration_section: RegistrationSection | null
    child_products: ChildProduct[]
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

export async function queryDashboard(args: { companyId: number }) {
    const response = await fetch(
        `${HOST}/api/dashboard/${args.companyId ?? ""}`
    )
    const result = (await response.json()) as DashboardResponse
    return result
}

/**
 * useDashboard contains all information about the company
 * logged in, such as sales contract, company information,
 * their configuration, etc...
 */
export function useDashboard() {
    const navigation = useNavigate()
    const queryClient = new QueryClient()
    const { companyId: rawCompanyId } = useParams({ from: "/$companyId" })

    // Check that if company is defined it is a positive number, otherwise set it to -1 to indicate that it is not a valid company
    const companyId = isNaN(Number(rawCompanyId)) ? -1 : Number(rawCompanyId)
    const queryKey = ["dashboard", companyId]

    const args = useQuery({
        queryKey,
        queryFn: async ({ queryKey: [, companyId] }) =>
            queryDashboard({ companyId: companyId as number }),
        enabled: companyId > 0
    })

    function invalidate() {
        queryClient.invalidateQueries({
            queryKey
        })
    }

    // If user tries to access a company that either doesn't exist
    // or they don't have access to, send them to the not found page
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
            to: "/$companyId/*",
            replace: true,
            params: { companyId: "not_found" }
        })
    }

    return { ...args, invalidate }
}
