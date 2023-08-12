import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"
import { CompleteButton } from "../../shared/CompleteButton"

export function LogoFormPage() {
    return (
        <FormWrapper>
            <FormField.Image
                mapping="exhibitor.catalogue_logo_squared"
                label="Company Square Logo"
            />
            <FormField.Image
                mapping="exhibitor.catalogue_logo_freesize"
                label="Company Free Sized Logo"
            />

            <div className="mt-10 flex flex-1 justify-center">
                <CompleteButton />
            </div>
        </FormWrapper>
    )
}
