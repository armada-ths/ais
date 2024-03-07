import { Form } from "../form_types"
import { StureContactPage } from "./sture_contact.page"

export const form = {
    key: "sture",
    name: "Content for your booth",
    description:
        "Armada are pleased to once again present Sture™ as our fair partner. Sture can help you with all contents for your booth and make it stand out in a great way. They are on the frontier of fair furnishings both when it comes to technologies and sustainable production - a perfect fit for your Armada booth!",
    progression: "none",
    pages: [
        {
            id: "sture_contact_info",
            title: "Content for your booth",
            isDone: null,
            pageComponent: StureContactPage,
            hasNextButton: false,
            fields: []
        }
    ]
} as const satisfies Form
