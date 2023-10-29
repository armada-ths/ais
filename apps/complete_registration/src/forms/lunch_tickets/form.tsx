import { Form } from "../form_types"
import { ViewLunchTicketsPage } from "./lunch_tickets.page"
import { CreateLunchTicketsPage } from "./lunch_ticket_create.page"
import { selectField } from "../../store/form/form_selectors"
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils"

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
            getProgress: () => 0,
            fields: [
                {
                    mapping: "assigned_lunch_tickets"
                },
                {
                    mapping: "fair_days"
                },
                {
                    mapping: "unassigned_lunch_tickets"
                }
            ]
        },
        {
            id: "create_ticket",
            title: "Create a new ticket",
            hasNextButton: false,
            hasPrevButton: false,
            pageComponent: CreateLunchTicketsPage,
            getProgress: state => {
                const unassigned =
                    (selectField(state, "unassigned_lunch_tickets")
                        ?.value as number) ?? 0
                const assigned = (
                    (selectField(state, "assigned_lunch_tickets")?.value ??
                        []) as LunchTicket[]
                ).length
                if (
                    typeof unassigned == "number" &&
                    typeof assigned == "number"
                ) {
                    return assigned / (assigned + unassigned)
                }
                return 0
            },
            fields: [
                {
                    mapping: "unassigned_lunch_tickets"
                },
                {
                    mapping: "fair_days"
                },
                {
                    mapping: "lunch_times"
                },
                {
                    mapping: "dietary_restrictions"
                }
            ]
        }
    ]
}
export default form
