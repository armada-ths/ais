import { HOST, RegistrationSection } from "@/shared/vars"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { useNavigate, useParams } from "@tanstack/react-router"

export enum RegistrationPeriod {
    BeforeIr = "before_initial_registration",
    InitialRegistration = "initial_registration",
    BetweenIrAndCr = "between_ir_and_cr",
    CompleteRegistration = "complete_registration",
    AfterCompleteRegistration = "after_complete_registration",
    Fair = "fair",
    AfterFair = "after_fair"
}
export enum SigningStep {
    UNSIGNED_IR = "unsigned_ir", // Unsigned, company has not yet signed the initial registration
    SIGNED_IR = "signed_ir", // Company has signed the initial registration
    SIGNED_CR = "signed_cr" // Company has signed the complete registration
}
export enum ApplicationStatus {
    NONE = "none", // None, no application status (SingingStep.UNSIGNED_IR)
    PENDING = "pending", //  Pending, company has not yet been accepted or rejected by armada
    ACCEPTED = "accepted", // Accepted, company has explicitly been accepted by armada
    REJECTED = "rejected", // Rejected, company has explicitly been rejected by armada
    WAITLIST = "waitlist", // Company is on the waitlist as a backup
    UNKNOWN = "unknown" // Unknown, there was an error on the backend (should not happen)
}

export interface DashboardResponse {
    period: RegistrationPeriod
    application_status: ApplicationStatus
    deadline: string
    fair: RegistrationFair
    ir_contract: Contract
    cr_contract: Contract
    ir_signature: Signature | null
    cr_signature: Signature | null
    sales_contacts: SalesContact[]
    orders: Order[]
    contact: Contact | null
    exhibitor: Exhibitor | null
    company: Company
    products: Product[]
    interested_in: Array<{ id: number }>
}

export interface Exhibitor {
    catalogue_about: string | null
    catalogue_cities: null
    catalogue_contact_email_address: string
    catalogue_contact_name: string | null
    catalogue_contact_phone_number: string | null
    catalogue_employments: Array<{
        id: number
        employment: string
        include_in_form: boolean
        selected: boolean
    }>
    catalogue_industries: Array<{
        id: number
        industry: string
        include_in_form: boolean
        selected: boolean
        category: number
    }>
    catalogue_locations: Array<{
        id: number
        location: string
        include_in_form: boolean
        selected: boolean
    }>
    catalogue_logo_freesize: string | null
    catalogue_logo_squared: string | null
    deadline_complete_registration: null
    id: number
    transport_comment: string | null
    transport_from: string
    transport_information_read: boolean
    transport_to: string
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

export interface ProductRegistrationSection {
    id: string
    name: RegistrationSection
    description: string
    hide_from_registration: boolean
}

export interface ChildProduct {
    quantity: number
    child_product: Omit<Product, "child_products" | "specific_products">
}

export interface Product {
    id: number
    name: string
    short_name: string
    max_quantity?: number
    unit_price: number
    description: string
    category: Category | null
    display_in_product_list: boolean
    registration_section: ProductRegistrationSection | null
    child_products: ChildProduct[]
    specific_products: Array<{
        unit_price: number
        specific_product: Omit<Product, "child_products" | "specific_products">
    }>
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

export interface Signature {
    timestamp: string
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
    const queryClient = useQueryClient()
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

    function updateCache(data: DashboardResponse) {
        queryClient.setQueryData(queryKey, data)
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

    return { ...args, invalidate, updateCache }
}
