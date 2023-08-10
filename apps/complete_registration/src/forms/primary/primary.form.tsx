import { Form } from "../../screens/form/screen"
import { selectSelectedProducts } from "../../store/products/products_selectors"

export const form: Form = {
    key: "primary",
    name: "Mandatory Information",
    description: "This is mandatory",
    isSkippable: false,
    pages: [
        {
            id: "package",
            title: "Select Package",
            hasNextButton: false,
            hasPrevButton: false,
            getProgress(state) {
                return selectSelectedProducts(state).find(
                    current => current.isPackage
                ) != null
                    ? 100
                    : 0
            },
            fields: []
        },
        {
            id: "events",
            title: "Select Events",
            fields: []
        },
        {
            id: "extras",
            title: "Select Extras",
            fields: []
        },
        {
            id: "invoice",
            title: "Invoice Information",
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
                    includeInProgressionSummary: false
                },
                {
                    mapping: "company.invoice_address_line_3",
                    includeInProgressionSummary: false
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
            fields: []
        }
    ]
}
