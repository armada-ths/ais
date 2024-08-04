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
        "initial_registration:::unsigned_ir:::*": CardStatus.Shown,
        "between_ir_and_cr:::unsigned_ir:::*": CardStatus.Shown,
        "complete_registration:::unsigned_ir:::*": CardStatus.Shown
    },
    ir_additional_info: {
        "*:::*:::*": CardStatus.Shown
    },
    exhibitor_catalog: {
        "initial_registration:::!unsigned_ir:::*": CardStatus.Shown,
        "between_ir_and_cr:::!unsigned_ir:::*": CardStatus.Shown,
        "complete_registration:::!unsigned_ir:::*": CardStatus.Shown,
        "after_complete_registration:::signed_cr:::*": CardStatus.Shown
    },
    fr_accounting: {
        "complete_registration:::signed_ir:::pending": CardStatus.Shown,
        "complete_registration:::signed_ir:::waitlist": CardStatus.Shown,
        "complete_registration:::signed_ir:::accepted": CardStatus.Shown
    },
    receipt: {
        "*:::signed_cr:::*": CardStatus.Shown
    },
    core_values: {
        "*:::signed_cr:::*": CardStatus.Shown
    },
    transport: {
        "*:::signed_cr:::accepted": CardStatus.Shown
    },
    sture: {
        "*:::signed_cr:::accepted": CardStatus.Shown
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
