import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"

export function LogoFormPage() {
    return (
        <FormWrapper>
            <div className="rounded bg-orange-100 p-3">
                <p className="text-orange-500">
                    File formats must be: (.png, .jpg or .gif)
                </p>
            </div>
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
