import { Form } from "../form_types"
import { CreateLunchTicketsPage } from "./lunch_ticket_create.page"
import { ViewLunchTicketsPage } from "./lunch_tickets.page"

export const form = {
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
            isDone: null,
            pageComponent: ViewLunchTicketsPage,
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
            isDone: null,
            pageComponent: CreateLunchTicketsPage,
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
} as const satisfies Form
