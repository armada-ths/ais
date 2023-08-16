import { FormField } from "../../screens/form/FormInput"
import { FormWrapper } from "../FormWrapper"

type InvoiceDetailsFormPageProps = {
    readOnly?: boolean
}

export function InvoiceDetailsFormPage({ readOnly }: InvoiceDetailsFormPageProps) {
    return (
        <FormWrapper>
            <FormField.Text
                label="Identity Number"
                mapping="company.identity_number"
                className="mb-10"
                readOnly={readOnly}
            />
            <FormField.Text
                label="Invoice Name"
                mapping="company.invoice_name"
                readOnly={readOnly}
            />
            <FormField.Text
                label="Invoice Email Address"
                mapping="company.invoice_email_address"
                readOnly={readOnly}
            />
            <div className="-mx-5 mt-10 flex flex-wrap gap-x-5 border-2 p-5 lg:grid lg:grid-cols-2">
                <p className="col-span-2 text-lg text-slate-700">
                    Invoice addresses, only one is required
                </p>
                <FormField.Text
                    label="Invoice Address"
                    mapping="company.invoice_address_line_1"
                    readOnly={readOnly}
                />
                <FormField.Text
                    label="Invoice Address 2"
                    mapping="company.invoice_address_line_2"
                    readOnly={readOnly}
                />
                <FormField.Text
                    label="Invoice Address 3"
                    mapping="company.invoice_address_line_3"
                    readOnly={readOnly}
                />
            </div>
            <div className="flex flex-wrap gap-x-5 lg:grid lg:grid-cols-2">
                <FormField.Text
                    label="Invoice Zip Code"
                    mapping="company.invoice_zip_code"
                    readOnly={readOnly}
                />
                <FormField.Text
                    label="Invoice City"
                    mapping="company.invoice_city"
                    readOnly={readOnly}
                />
                <FormField.Text
                    label="Invoice Country"
                    mapping="company.invoice_country"
                    readOnly={readOnly}
                />
            </div>
            <FormField.Text
                label="Invoice Reference"
                mapping="company.invoice_reference"
                readOnly={readOnly}
            />
        </FormWrapper>
    )
}
