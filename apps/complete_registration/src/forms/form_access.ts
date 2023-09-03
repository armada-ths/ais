import { FORMS } from "."
import { RegistrationStatus } from "../store/company/company_slice"

export const FORM_OPEN_DURING: Record<
    keyof typeof FORMS,
    RegistrationStatus[]
> = {
    primary: ["complete_registration"],
    receipt: ["complete_registration_signed"],
    lunch_tickets: ["complete_registration_signed"],
    exhibitor_catalog: [
        "complete_registration_signed",
        "complete_registration",
        "before_complete_registration"
    ],
    transport: ["complete_registration", "complete_registration_signed"],
    banquet_tickets: ["complete_registration_signed"],
    sture: ["complete_registration", "complete_registration_signed"]
}

export const FORM_HIDDEN_DURING: Partial<
    Record<keyof typeof FORMS, RegistrationStatus[]>
> = {
    primary: ["complete_registration_signed"],
    receipt: ["complete_registration"]
}

export function isFormOpen(
    form: keyof typeof FORMS,
    status: RegistrationStatus | null
): boolean {
    if (!status) return false
    return FORM_OPEN_DURING[form]?.includes(status)
}
export function isFormHidden(
    form: keyof typeof FORMS,
    status: RegistrationStatus | null
): boolean {
    if (!status) return false
    return FORM_HIDDEN_DURING[form]?.includes(status) ?? false
}
