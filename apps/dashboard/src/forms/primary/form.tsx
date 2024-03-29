import { FormSidebarCartSummary } from "@/screens/form/sidebar/FormSidebarCartSummary"
import {
    selectProductEvents,
    selectProductExtras
} from "@/store/products/products_selectors"
import { Form } from "../form_types"
import { InvoiceDetailsFormPage } from "./invoice_details.page"
import { PackageSelectFormPage } from "./package_select.page"
import { ProductFormPage } from "./product.page"
import { SummaryFormPage } from "./summary.page"

export const form = {
    key: "primary",
    name: "Order & Invoice Details",
    description:
        "On this page you select products and entry of company invoice details. Once submitted, no changes are permitted.",
    rightSidebar: FormSidebarCartSummary,
    pages: [
        {
            id: "packages",
            title: "Select Package",
            hasNextButton: false,
            hasPrevButton: false,
            isDone: null,
            pageComponent: PackageSelectFormPage
        },
        {
            id: "events",
            title: "Select Events",
            hasPrevButton: false,
            isDone: null,
            pageComponent: () => (
                <ProductFormPage selector={selectProductEvents} />
            )
        },
        {
            id: "extras",
            title: "Select Extras",
            isDone: null,
            pageComponent: () => (
                <ProductFormPage selector={selectProductExtras} />
            )
        },
        {
            id: "invoice",
            title: "Invoice Information",
            pageComponent: () => <InvoiceDetailsFormPage />,
            isDone: null,
            fields: [
                {
                    mapping: "company.invoice_name"
                },
                {
                    mapping: "company.invoice_email_address"
                },
                {
                    mapping: "company.identity_number"
                },
                {
                    mapping: "company.invoice_address_line_1"
                },
                {
                    mapping: "company.invoice_address_line_2",
                    mandatory: false
                },
                {
                    mapping: "company.invoice_address_line_3",
                    mandatory: false
                },
                {
                    mapping: "company.invoice_zip_code"
                },
                {
                    mapping: "company.invoice_city"
                },
                {
                    mapping: "company.invoice_country"
                },
                {
                    mapping: "company.invoice_reference"
                }
            ]
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
