import IrContactPage from "@/forms/ir_additional_info/ir_company_contact.page"
import IrAdditionalInfoPage from "@/forms/ir_additional_info/ir_company_info.page"
import { Form } from "../form_types"

export const form: Form = {
    key: "ir_additional_info",
    name: "Additional Information",
    description: "Provide additional information about the company",
    pages: [
        {
            id: "ir_additional_info_company_details",
            title: "Company Details",
            pageComponent: IrAdditionalInfoPage,
            isDone: ({ registration }) =>
                registration.company.name != null &&
                registration.company.identity_number != null
        },
        {
            id: "ir_additional_info_contact_person",
            title: "Contact Person",
            pageComponent: IrContactPage,
            hasNextButton: false,
            isDone: ({ registration }) =>
                registration.contact.first_name != null &&
                registration.contact.last_name != null &&
                registration.contact.email_address != null
        }
    ]
}