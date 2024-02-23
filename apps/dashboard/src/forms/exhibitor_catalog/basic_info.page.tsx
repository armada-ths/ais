import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"

export function BasicInfoFormPage() {
    return (
        <FormWrapper>
            <FormField.TextArea
                mapping="exhibitor.catalogue_about"
                label="Text about your organisation (required to sign contract)"
            />
            <p className="mt-1 text-sm">
                Keep it concise - no more than 600 characters. Please write in
                english to reach both Swedish and international students.
            </p>
            <FormField.Text
                label="Please write the main cities where your company operates"
                mapping="exhibitor.catalogue_cities"
                className="mt-14"
            />
            <p className="mt-1 text-sm">
                Separate the cities with commas. Eg: Stockholm,Gothenburg,Malmö
            </p>
            <div className="-mx-5 mt-10 grid grid-cols-2 gap-x-5 border-2 px-5 pb-5">
                <FormField.Text
                    mapping="exhibitor.catalogue_contact_name"
                    label="Contact Person Name"
                />
                <FormField.Text
                    mapping="exhibitor.catalogue_contact_email_address"
                    label="Contact Person Email"
                />
                <FormField.Text
                    mapping="exhibitor.catalogue_contact_phone_number"
                    label="Contact Person Phone Number"
                />
            </div>
        </FormWrapper>
    )
}
