import { form as PrimaryForm } from "./primary/form"
import CreateLunchTicketsForm from "./create_lunch_tickets/form"
import { form as ExhibitorCatalogForm } from "./exhibitor_catalog/form"
import { form as TransportForm } from "./transport/form"

export function getMutableFormsInstance() {
    return {
        primary: PrimaryForm,
        lunch_tickets: CreateLunchTicketsForm,
        exhibitor_catalog: ExhibitorCatalogForm,
        transport: TransportForm
    }
}
export const FORMS = Object.freeze(getMutableFormsInstance())
