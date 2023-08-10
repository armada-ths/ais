import { FormField } from "../screens/form/FormInput"
import { Form } from "../screens/form/screen"

export const form: Form = {
    name: "Mandatory Information",
    description: "This is mandatory",
    isSkippable: false,
    pages: [
        {
            id: "primary_form",
            title: "Invoice Information",
            fields: [
                {
                    mapping: "company.invoice_name",
                    component: (
                        <FormField.Text
                            label="Invoice Name"
                            mapping="company.invoice_name"
                            className="flex-1 basis-2/5"
                        />
                    )
                },
                {
                    mapping: "company.invoice_email_address",
                    component: (
                        <FormField.Text
                            label="Invoice Email Address"
                            mapping="company.invoice_email_address"
                            className="flex-1 basis-2/5"
                        />
                    )
                },
                {
                    mapping: "company.identity_number",
                    component: (
                        <FormField.Text
                            label="Identity Number"
                            mapping="company.identity_number"
                        />
                    )
                },
                {
                    mapping: "company.invoice_address_line_1",
                    component: (
                        <FormField.Text
                            label="Invoice Address"
                            mapping="company.invoice_address_line_1"
                            className="flex-1"
                        />
                    )
                },
                {
                    mapping: "company.invoice_address_line_2",
                    component: (
                        <FormField.Text
                            label="Invoice Address 2 (optional)"
                            mapping="company.invoice_address_line_2"
                            className="flex-1"
                        />
                    )
                },
                {
                    mapping: "company.invoice_address_line_3",
                    component: (
                        <FormField.Text
                            label="Invoice Address 3 (optional)"
                            mapping="company.invoice_address_line_3"
                        />
                    )
                },
                {
                    mapping: "company.invoice_zip_code",
                    component: (
                        <FormField.Text
                            label="Invoice Zip Code"
                            mapping="company.invoice_zip_code"
                            className="flex-1 basis-2/5"
                        />
                    )
                },
                {
                    mapping: "company.invoice_city",
                    component: (
                        <FormField.Text
                            label="Invoice City"
                            mapping="company.invoice_city"
                            className="flex-1 basis-2/5"
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
            fields: [
                {
                    mapping: "company.general_email_address",
                    component: (
                        <FormField.Text
                            label="General email address"
                            mapping="company.general_email_address"
                        />
                    )
                }
            ]
        }
    ]
}
