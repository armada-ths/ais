import { Form } from "../form_types"
import { ViewLunchTicketsPage } from "./lunch_tickets.page"
import { CreateLunchTicketsPage } from "./lunch_ticket_create.page"

const form: Form = {
    key: "lunch_tickets",
    name: "Lunch Tickets",
    description:
        "Lunch tickets give attendees access to the lunch area at the fair",
    progression: "none",
    pages: [
        {
            id: "view_ticket",
            title: "Company Lunch Tickets",
            hasNextButton: false,
            hasPrevButton: false,
            pageComponent: ViewLunchTicketsPage,
        },
        {
            id: "create_ticket",
            title: "Create a new ticket",
            hasNextButton: false,
            hasPrevButton: false,
            pageComponent: CreateLunchTicketsPage,
        }
    ]
}
export default form
