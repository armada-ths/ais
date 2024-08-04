import { belongsToSection } from "@/forms/fr_accounting/accounting_utilities"
import { FormSidebarCartSummary } from "@/screens/form/sidebar/FormSidebarCartSummary"
import { RegistrationSection } from "@/shared/vars"
import { Form } from "../form_types"
import { InvoiceDetailsFormPage } from "./invoice_details.page"
import { PackageSelectFormPage } from "./package_select.page"
import { ProductFormPage } from "./product.page"
import { SummaryFormPage } from "./summary.page"

export const form = {
    key: "fr_accounting",
    name: "Order & Invoice Details",
    description:
        "On this page you select products and entry of company invoice details. Once submitted, no changes are permitted.",
    rightSidebar: FormSidebarCartSummary,
    pages: [
        {
            id: "packages",
            title: "Select Package",
            hasNextButton: true,
            hasPrevButton: false,
            isDone: ({ dashboard }) =>
                dashboard.orders.some(order =>
                    belongsToSection(
                        order.product,
                        RegistrationSection.Packages
                    )
                ),
            pageComponent: PackageSelectFormPage
        },
        {
            id: "events",
            title: "Select Events",
            isDone: null,
            pageComponent: () => (
                <ProductFormPage section={RegistrationSection.Events} />
            )
        },
        {
            id: "extras",
            title: "Select Extras",
            isDone: null,
            pageComponent: () => (
                <ProductFormPage section={RegistrationSection.Extras} />
            )
        },
        {
            id: "invoice",
            title: "Invoice Information",
            pageComponent: () => <InvoiceDetailsFormPage />,
            isDone: ({ dashboard }) =>
                dashboard.company.identity_number != null &&
                dashboard.company.invoice_name != null &&
                dashboard.company.invoice_email_address != null &&
                dashboard.company.invoice_address_line_1 != null &&
                dashboard.company.invoice_zip_code != null &&
                dashboard.company.invoice_city != null &&
                dashboard.company.invoice_country != null
        },
        {
            id: "summary",
            title: "Summary",
            hasNextButton: false,
            isDone: null,
            pageComponent: SummaryFormPage
        }
    ]
} satisfies Form
