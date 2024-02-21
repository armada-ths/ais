import { form as CoreValues } from "./core_values/form"
import { form as ExhibitorCatalogForm } from "./exhibitor_catalog/form"
import { form as IrSignupForm } from "./ir_signup/form"
import CreateLunchTicketsForm from "./lunch_tickets/form"
import { form as PrimaryForm } from "./primary/form"
import { form as ReceiptForm } from "./receipt/form"
import { form as StureForm } from "./sture/form"
import { form as TransportForm } from "./transport/form"

export function getMutableFormsInstance() {
    return {
        ir_signup: IrSignupForm,
        primary: PrimaryForm,
        receipt: ReceiptForm,
        exhibitor_catalog: ExhibitorCatalogForm,
        transport: TransportForm,
        lunch_tickets: CreateLunchTicketsForm,
        sture: StureForm,
        core_values: CoreValues
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
