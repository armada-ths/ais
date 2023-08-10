import { Form } from "../../screens/form/screen"
import { selectSelectedProducts } from "../../store/products/products_selectors"
import { PACKAGE_KEY } from "../../store/products/products_slice"

export const form: Form = {
    key: "primary",
    name: "Mandatory Information",
    description: "This is mandatory",
    isSkippable: false,
    pages: [
        {
            id: "package",
            title: "Select Package",
            hasPageControls: false,
            getProgress(state) {
                return selectSelectedProducts(state).find(
                    current => current.category.name === PACKAGE_KEY
                ) != null
                    ? 100
                    : 0
            },
            fields: [
                {
                    mapping: "company.general_email_address"
                }
            ]
        },
        {
            id: "primary_form",
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
                    mapping: "company.invoice_address_line_2"
                },
                {
                    mapping: "company.invoice_address_line_3"
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
            id: "general_form",
            title: "ANother page",
            fields: [
                {
                    mapping: "company.general_email_address"
                }
            ]
        }
    ]
}
