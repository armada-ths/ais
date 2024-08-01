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
// PERIOD:::EXHIBITOR_STATE
export const FORM_ACCESS: FormAccessDeclaration = {
    ir_signup: {
        "*:::unsigned_ir": CardStatus.Shown,
        "initial_registration:::!unsigned_ir": CardStatus.ShownLocked,
        "between_ir_and_cr:::!unsigned_ir": CardStatus.ShownLocked
    },
    ir_additional_info: {
        "initial_registration:::!unsigned_ir": CardStatus.Shown,
        "between_ir_and_cr:::!unsigned_ir": CardStatus.Shown
    },
    exhibitor_catalog: {
        "between_ir_and_cr:::*": CardStatus.Shown,
        "complete_registration:::*": CardStatus.Shown,
        "after_complete_registration:::*": CardStatus.Shown
    },
    fr_accounting: {
        "complete_registration:::rejected": CardStatus.HiddenLocked,
        "complete_registration:::signed_cr": CardStatus.HiddenLocked,
        "complete_registration:::*": CardStatus.Shown
    },
    receipt: {
        "*:::signed_cr": CardStatus.HiddenLocked
    },
    core_values: {
        "*:::signed_cr": CardStatus.Shown
    },
    transport: {
        "*:::signed_cr": CardStatus.Shown
    },
    sture: {
        "*:::signed_cr": CardStatus.Shown
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
