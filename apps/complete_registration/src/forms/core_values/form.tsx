import { Form } from "../form_types"
import { DiversityIndexPage } from "./diversity_index.page"

export const form: Form = {
    key: "core_values",
    name: "Core Values",
    description: "Core values and very important stuff",
    progression: "none",
    pages: [
        {
            id: "sture_contact_info",
            title: "Diversity Index",
            pageComponent: DiversityIndexPage,
            hasNextButton: false,
            fields: []
        }
    ]
}
