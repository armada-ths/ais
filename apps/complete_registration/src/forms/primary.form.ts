import { Form } from "../screens/form/screen"

export const form: Form = {
    name: "Mandatory info",
    description: "This is mandatory",
    isSkippable: false,
    pages: [
        {
            id: "primary_form",
            title: "Billing info",
            fields: [
                {
                    mapping: "company.identity_number",
                    type: "input-text",
                    name: "Identity number"
                },
                {
                    mapping: "company.invoice_city",
                    type: "input-text",
                    name: "Invoice City"
                },
                {
                    mapping: "company.general_email_address",
                    type: "input-text",
                    name: "General email address"
                },
                {
                    mapping: "company.invoice_country",
                    type: "input-text",
                    name: "Invoice country"
                }
            ]
        },
        {
            id: "primary_form_second",
            title: "ANother page",
            fields: []
        }
    ]
}
