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

export function getFieldFromForm(forms: typeof FORMS, mapping: string) {
    // Iterate over all forms and pages to find the field with the given mapping
    for (const formMeta of Object.values(forms)) {
        for (const page of formMeta.pages) {
            const field = page.fields?.find(f => f.mapping == mapping) ?? 0
            if (field) return field
        }
    }
    return null
}
