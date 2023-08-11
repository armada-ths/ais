import { Form } from "../../screens/form/screen"
import { BasicInfoFormPage } from "./basic_info.page"
import { LogoFormPage } from "./logo.page"

export const form: Form = {
    key: "exhibitor_catalog",
    name: "Exhibitor Catalog",
    description:
        "This information is used in the exhibitor catalogue on the website and for matching relevant students with your company. We encourage you to fill out as many fields as possible to increase the likelihood of receiving relevant matches.",
    isSkippable: true,
    pages: [
        {
            id: "basic_info",
            title: "Basic Info",
            pageComponent: BasicInfoFormPage,
            fields: [
                {
                    mapping: "exhibitor.catalogue_about"
                },
                {
                    mapping: "exhibitor.catalogue_cities"
                },
                {
                    mapping: "exhibitor.catalogue_contact_name"
                },
                {
                    mapping: "exhibitor.catalogue_contact_email_address"
                },
                {
                    mapping: "exhibitor.catalogue_contact_phone_number"
                }
            ]
        },
        {
            id: "logo",
            title: "Logo",
            hasNextButton: false,
            pageComponent: LogoFormPage,
            fields: [
                {
                    mapping: "exhibitor.catalogue_logo_squared"
                },
                {
                    mapping: "exhibitor.catalogue_logo_freesize",
                    mandatory: false
                }
            ]
        }
    ]
}
