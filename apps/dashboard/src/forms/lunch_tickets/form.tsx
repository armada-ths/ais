import { LunchTicketLink } from "@/forms/lunch_tickets/lunch_ticket_link"
import { Form } from "../form_types"

export const form = {
    key: "lunch_tickets",
    name: "Lunch tickets form",
    description:
        "Sign up for lunch tickets at the fair, assign dietary preferences and allergies.",
    progression: "none",
    pages: [
        {
            id: "sture_contact_info",
            title: "Lunch tickets form",
            isDone: null,
            pageComponent: LunchTicketLink,
            hasNextButton: false,
            fields: []
        }
    ]
} as const satisfies Form
