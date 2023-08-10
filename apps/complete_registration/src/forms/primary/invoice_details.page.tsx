import { FormField } from "../../screens/form/FormInput"
import { FormWrapper } from "../FormWrapper"

export function InvoiceDetailsFormPage() {
    return (
        <FormWrapper>
            <FormField.Text
                label="Identity Number"
                mapping="company.identity_number"
                className="mb-10"
            />
            <div className="flex flex-wrap gap-x-5 lg:grid lg:grid-cols-2">
                <FormField.Text
                    label="Invoice Address"
                    mapping="company.invoice_address_line_1"
                />
                <FormField.Text
                    label="Invoice Address 2 (optional)"
                    mapping="company.invoice_address_line_2"
                />
                <FormField.Text
                    label="Invoice Address 3 (optional)"
                    mapping="company.invoice_address_line_3"
                />
            </div>
            <div className="mt-10 flex flex-wrap gap-x-5 lg:grid lg:grid-cols-2">
                <FormField.Text
                    label="Invoice Zip Code"
                    mapping="company.invoice_zip_code"
                />
                <FormField.Text
                    label="Invoice City"
                    mapping="company.invoice_city"
                />
                <FormField.Text
                    label="Invoice Country"
                    mapping="company.invoice_country"
                />
            </div>
            <FormField.Text
                label="Invoice Reference"
                mapping="company.invoice_reference"
                className="mt-16"
            />
        </FormWrapper>
    )
}
