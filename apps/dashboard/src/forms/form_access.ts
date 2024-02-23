import { FORMS } from "."
import { RegistrationStatus } from "../store/company/company_slice"

// If not specified hidden_locked is default
export const FORM_ACCESS: Record<
    RegistrationStatus,
    Partial<
        Record<keyof typeof FORMS, "shown" | "shown_locked" | "hidden_locked">
    >
> = {
    before_initial_registration: {},
    initial_registration: {
        ir_signup: "shown"
    },
    initial_registration_signed: {
        ir_signup: "shown_locked",
        ir_additional_info: "shown"
    },
    after_initial_registration: {
        ir_signup: "shown_locked"
    },
    after_initial_registration_signed: {
        ir_signup: "shown_locked",
        ir_additional_info: "shown"
    },
    after_initial_registration_acceptance_accepted: {
        ir_signup: "shown_locked",
        ir_additional_info: "shown"
    },
    after_initial_registration_acceptance_rejected: {
        ir_signup: "shown_locked",
        ir_additional_info: "shown"
    },
    before_complete_registration_ir_signed: {
        lunch_tickets: "shown",
        exhibitor_catalog: "shown",
        core_values: "shown"
    }, // FR "Active" but no contract exists
    before_complete_registration_ir_unsigned: {
        lunch_tickets: "shown",
        exhibitor_catalog: "shown",
        core_values: "shown"
    }, // FR "Active" but no contract exists
    complete_registration_ir_signed: {
        primary: "shown",
        lunch_tickets: "shown",
        transport: "shown",
        sture: "shown",
        core_values: "shown"
    },
    complete_registration_ir_unsigned: {
        primary: "shown",
        lunch_tickets: "shown",
        transport: "shown",
        sture: "shown",
        core_values: "shown"
    },
    complete_registration_signed: {
        receipt: "shown",
        lunch_tickets: "shown",
        exhibitor_catalog: "shown",
        transport: "shown",
        sture: "shown",
        core_values: "shown"
    },
    after_complete_registration: {
        lunch_tickets: "shown",
        exhibitor_catalog: "shown",
        transport: "shown",
        sture: "shown",
        core_values: "shown"
    },
    after_complete_registration_signed: {
        lunch_tickets: "shown",
        exhibitor_catalog: "shown",
        transport: "shown",
        sture: "shown",
        core_values: "shown"
    }
}

/* export const FORM_OPEN_DURING: Record<
    keyof typeof FORMS,
    RegistrationStatus[]
> = {
    ir_signup: ["initial_registration"],
    primary: ["complete_registration"],
    receipt: [
        "complete_registration_signed",
        "after_complete_registration_signed"
    ],
    lunch_tickets: [
        "complete_registration_signed",
        "complete_registration",
        "before_complete_registration",
        "after_complete_registration",
        "after_complete_registration_signed"
    ],
    exhibitor_catalog: [
        "complete_registration_signed",
        "complete_registration",
        "before_complete_registration",
        "after_complete_registration",
        "after_complete_registration_signed"
    ],
    transport: [
        "complete_registration",
        "complete_registration_signed",
        "after_complete_registration",
        "after_complete_registration_signed"
    ],
    sture: [
        "complete_registration",
        "complete_registration_signed",
        "after_complete_registration",
        "after_complete_registration_signed"
    ],
    core_values: [
        "before_complete_registration",
        "complete_registration",
        "complete_registration_signed",
        "after_complete_registration",
        "after_complete_registration_signed"
    ]
}

export const FORM_HIDDEN_DURING: Partial<
    Record<keyof typeof FORMS, RegistrationStatus[]>
> = {
    ir_signup: ["after_complete_registration"],
    primary: [
        "complete_registration_signed",
        "after_complete_registration",
        "after_complete_registration_signed"
    ],
    receipt: ["complete_registration"]
} */

export function isFormOpen(
    form: keyof typeof FORMS,
    status: RegistrationStatus | null
): boolean {
    if (!status) return false
    return FORM_ACCESS[status]?.[form] === "shown"
}
export function isFormVisible(
    form: keyof typeof FORMS,
    status: RegistrationStatus | null
): boolean {
    if (!status) return false
    return (
        FORM_ACCESS[status]?.[form] === "shown" ||
        FORM_ACCESS[status]?.[form] === "shown_locked"
    )
}
