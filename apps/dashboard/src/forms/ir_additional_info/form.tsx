import IrContactPage from "@/forms/ir_additional_info/ir_company_contact.page"
import IrAdditionalInfoPage from "@/forms/ir_additional_info/ir_company_info.page"
import { IrInterestedInPage } from "@/forms/ir_additional_info/ir_interested_in.page"
import { Form } from "../form_types"

export const form = {
    key: "ir_additional_info",
    name: "Additional Information",
    description: "Provide additional information about the company",
    pages: [
        {
            id: "ir_additional_info_interested_in",
            title: "Preferences",
            pageComponent: IrInterestedInPage,
            isDone: null
        },
        {
            id: "ir_additional_info_company_details",
            title: "Company Details",
            pageComponent: IrAdditionalInfoPage,
            isDone: ({ dashboard }) =>
                dashboard.company.name != null &&
                dashboard.company.identity_number != null
        },
        {
            id: "ir_additional_info_contact_person",
            title: "Contact Person",
            pageComponent: IrContactPage,
            hasNextButton: false,
            isDone: ({ dashboard }) =>
                dashboard.contact == null
                    ? null
                    : dashboard.contact.first_name != null &&
                      dashboard.contact.last_name != null &&
                      dashboard.contact.email_address != null
        }
    ]
} as const satisfies Form
