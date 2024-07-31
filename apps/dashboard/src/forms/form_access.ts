import {
    AccessDeclaration,
    AccessDeclarationArgs,
    parseAccessDeclaration
} from "@/forms/access_declaration_logic"
import { FORMS } from "."

export enum CardStatus {
    Shown = "shown",
    ShownLocked = "shown_locked",
    HiddenLocked = "hidden_locked"
}


type FormAccessDeclaration = Record<
    keyof typeof FORMS,
    Partial<Record<AccessDeclaration, CardStatus>>
>

// follows format
// PERIOD:::COMPANY_CONTRACT:::EXHIBITOR_ACCEPTANCE
export const FORM_ACCESS: FormAccessDeclaration = {
    ir_signup: {
        "initial_registration:::unsigned:::*": CardStatus.Shown,
        "initial_registration:::ir_signed:::*": CardStatus.ShownLocked,
        "between_ir_and_cr:::ir_signed:::*": CardStatus.ShownLocked
    },
    ir_additional_info: {
        "initial_registration:::ir_signed:::*": CardStatus.Shown
    },
    exhibitor_catalog: {
        "between_ir_and_cr:::*:::*": CardStatus.Shown,
        "complete_registration:::*:::*": CardStatus.Shown,
        "after_complete_registration:::*:::*": CardStatus.Shown
    },
    fr_accounting: {
        "complete_registration:::*:::*": CardStatus.Shown,
        "complete_registration:::*:::rejected": CardStatus.HiddenLocked,
        "complete_registration:::cr_signed:::*": CardStatus.HiddenLocked
    },
    receipt: {
        "complete_registration:::*:::*": CardStatus.HiddenLocked,
        "complete_registration:::cr_signed:::*": CardStatus.HiddenLocked
    },
    core_values: {
        "complete_registration:::cr_signed:::*": CardStatus.Shown
    },
    transport: {
        "complete_registration:::cr_signed:::*": CardStatus.Shown
    },
    sture: {
        "complete_registration:::cr_signed:::*": CardStatus.Shown
    }
}

export function isFormOpen(
    state: AccessDeclarationArgs | null,
    form: keyof typeof FORMS,
    formAccessDeclaration?: FormAccessDeclaration
): boolean {
    if (state == null) return false
    const formDeclaration = (formAccessDeclaration ?? FORM_ACCESS)[form]
    return (
        parseAccessDeclaration(state, formDeclaration)?.value ===
        CardStatus.Shown
    )
}
export function isFormVisible(
    state: AccessDeclarationArgs | null,
    form: keyof typeof FORMS
): boolean {
    if (state == null) return false
    const formDeclaration = FORM_ACCESS[form]
    return (
        parseAccessDeclaration(state, formDeclaration)?.value ===
            CardStatus.Shown ||
        parseAccessDeclaration(state, formDeclaration)?.value ===
            CardStatus.ShownLocked
    )
}
