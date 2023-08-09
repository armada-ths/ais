import { FormField } from "../screens/form/FormInput"
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
                    mapping: "company.identify_number",
                    component: (
                        <FormField.Text
                            label="Identity Number"
                            mapping="company.identify_number"
                        />
                    )
                },
                {
                    mapping: "company.invoice_city",
                    component: (
                        <FormField.Text
                            label="Company Name"
                            mapping="company.invoice_city"
                        />
                    )
                },
                {
                    mapping: "company.general_email_address",
                    component: (
                        <FormField.Text
                            label="General Email Address"
                            mapping="company.general_email_address"
                        />
                    )
                },
                {
                    mapping: "company.invoice_country",
                    component: (
                        <FormField.Text
                            label="Invoice Country"
                            mapping="company.invoice_country"
                        />
                    )
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
