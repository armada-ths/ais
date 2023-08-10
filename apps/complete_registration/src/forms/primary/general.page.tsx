import { FormField } from "../../screens/form/FormInput"

export function GeneralFormPage() {
    return (
        <div>
            <FormField.Text
                label="Invoice Reference"
                mapping="company.invoice_reference"
            />
        </div>
    )
}
