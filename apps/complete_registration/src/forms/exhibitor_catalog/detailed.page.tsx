import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"
import { CompleteButton } from "../../shared/CompleteButton"

export function DetailedFormPage() {
    return (
        <FormWrapper>
            <FormField.MultiSelect
                label="Your industries (Think about everything an interesting student might search for)"
                mapping="exhibitor.catalogue_industries"
                className="w-full"
                filter
                optionLabel="industry"
                optionValue="selected"
            />
            <FormField.MultiSelect
                label="What employment are you offering?"
                mapping="exhibitor.catalogue_employments"
                className="w-full"
                filter
                optionLabel="employment"
                optionValue="selected"
            />
            <FormField.MultiSelect
                label="Select your countries"
                mapping="exhibitor.catalogue_locations"
                className="w-full"
                filter
                optionLabel="location"
                optionValue="selected"
            />
            <div className="mt-10 flex justify-center">
                <CompleteButton />
            </div>
        </FormWrapper>
    )
}
