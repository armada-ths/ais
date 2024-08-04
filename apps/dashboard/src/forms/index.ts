import { form as CoreValues } from "./core_values/form"
import { form as ExhibitorCatalogForm } from "./exhibitor_catalog/form"
import { form as FrAccountingForm } from "./fr_accounting/form"
import { form as IrAdditionalInfo } from "./ir_additional_info/form"
import { form as IrSignupForm } from "./ir_signup/form"
//import { form as CreateLunchTicketsForm } from "./lunch_tickets/form"
import { form as ReceiptForm } from "./receipt/form"
import { form as StureForm } from "./sture/form"
import { form as TransportForm } from "./transport/form"

export function getMutableFormsInstance() {
    return {
        ir_signup: IrSignupForm,
        ir_additional_info: IrAdditionalInfo,
        fr_accounting: FrAccountingForm,
        receipt: ReceiptForm,
        exhibitor_catalog: ExhibitorCatalogForm,
        transport: TransportForm,
        //lunch_tickets: CreateLunchTicketsForm,
        sture: StureForm,
        core_values: CoreValues
    } as const
}
export const FORMS = {
    ir_signup: IrSignupForm,
    fr_accounting: FrAccountingForm, //
    receipt: ReceiptForm,
    ir_additional_info: IrAdditionalInfo,
    exhibitor_catalog: ExhibitorCatalogForm,
    transport: TransportForm,
    //lunch_tickets: CreateLunchTicketsForm, //
    sture: StureForm,
    core_values: CoreValues
} as const

export type FormIds = keyof typeof FORMS
export type FormPageIds =
    (typeof FORMS)[keyof typeof FORMS]["pages"][number]["id"]

/**
 * @deprecated
 */
export function getFieldFromForm(forms: typeof FORMS, mapping: string) {
    // Iterate over all forms and pages to find the field with the given mapping
    for (const formMeta of Object.values(forms)) {
        for (const page of formMeta.pages) {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            const field = page.fields?.find(f => f.mapping == mapping) ?? 0
            if (field) return field
        }
    }
    return null
}
