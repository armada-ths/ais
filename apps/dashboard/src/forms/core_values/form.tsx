import { Form } from "../form_types"
import { DiversityIndexPage } from "./diversity_index.page"

export const form = {
    key: "core_values",
    name: "Core Values",
    description:
        "Allow students to understand your values better. Complete the form for an opportunity to join our Diversity Focus Room.",
    progression: "none",
    pages: [
        {
            id: "sture_contact_info",
            title: "Diversity Index",
            isDone: null,
            pageComponent: DiversityIndexPage,
            hasNextButton: false,
            fields: []
        }
    ]
} as const satisfies Form
