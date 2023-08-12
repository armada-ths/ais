import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"

export function DetailedFormPage() {
    return (
        <FormWrapper>
            <FormField.MultiSelect
                label="Industries"
                mapping="exhibitor.catalogue_industries"
                className="w-full"
                filter
                optionLabel="industry"
                optionValue="selected"
            />
        </FormWrapper>
    )
}
