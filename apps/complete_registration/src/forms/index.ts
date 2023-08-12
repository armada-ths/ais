import { form as PrimaryForm } from "./primary/form"
import CreateLunchTicketsForm from "./lunch_tickets/form"
import { form as ExhibitorCatalogForm } from "./exhibitor_catalog/form"
import { form as TransportForm } from "./transport/form"
import { form as BanquetForm } from "./banquet/form"

export function getMutableFormsInstance() {
    return {
        primary: PrimaryForm,
        exhibitor_catalog: ExhibitorCatalogForm,
        transport: TransportForm,
        lunch_tickets: CreateLunchTicketsForm,
        banquet_tickets: BanquetForm
    }
}
export const FORMS = Object.freeze(getMutableFormsInstance())
