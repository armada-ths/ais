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
