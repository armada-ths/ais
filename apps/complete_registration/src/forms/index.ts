import { form as PrimaryForm } from "./primary/form"
import CreateLunchTicketsForm from "./create_lunch_tickets/form"

export function getMutableFormsInstance() {
    return {
        primary: PrimaryForm,
        create_lunch_tickets: CreateLunchTicketsForm
    }
}
export const FORMS = Object.freeze(getMutableFormsInstance())
