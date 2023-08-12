import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"

export function LogoFormPage() {
    return (
        <FormWrapper>
            <FormField.Image
                mapping="exhibitor.catalogue_logo_squared"
                label="Company Logo Square"
            />
            <FormField.Image
                mapping="exhibitor.catalogue_logo_freesize"
                label="Company Free Sized Logo (optional)"
            />
        </FormWrapper>
    )
}
