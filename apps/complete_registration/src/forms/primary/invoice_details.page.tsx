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
            <FormField.Text
                label="Invoice Name"
                mapping="company.invoice_name"
            />
            <FormField.Text
                label="Invoice Email Address"
                mapping="company.invoice_email_address"
            />
            <div className="-mx-5 mt-10 flex flex-wrap gap-x-5 border-2 p-5 lg:grid lg:grid-cols-2">
                <p className="col-span-2 text-lg text-slate-700">
                    Invoice addresses, only one is required
                </p>
                <FormField.Text
                    label="Invoice Address"
                    mapping="company.invoice_address_line_1"
                />
                <FormField.Text
                    label="Invoice Address 2"
                    mapping="company.invoice_address_line_2"
                />
                <FormField.Text
                    label="Invoice Address 3"
                    mapping="company.invoice_address_line_3"
                />
            </div>
            <div className="flex flex-wrap gap-x-5 lg:grid lg:grid-cols-2">
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
            />
        </FormWrapper>
    )
}
