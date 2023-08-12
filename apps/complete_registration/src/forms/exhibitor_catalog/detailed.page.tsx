import React from "react"
import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"

export function DetailedFormPage() {
    return (
        <FormWrapper>
            <FormField.MultiSelect
                label=""
                mapping="exhibitor.catalogue_industries"
                options={[
                    {
                        label: "First",
                        value: "first"
                    },
                    {
                        label: "Second",
                        value: "third"
                    }
                ]}
            />
        </FormWrapper>
    )
}
