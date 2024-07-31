import {
    ApplicationStatus,
    RegistrationPeriod
} from "@/shared/hooks/api/useDashboard"

export enum SignupState {
    Unsigned = "unsigned",
    IrSigned = "ir_signed",
    CrSigned = "cr_signed"
}

export type AccessDeclaration = `${RegistrationPeriod | "*"}:::${
    | SignupState
    | "*"}:::${ApplicationStatus | "*"}`

export interface AccessDeclarationArgs {
    period: RegistrationPeriod
    exhibitorStatus: ApplicationStatus
    signupState: SignupState
}

export function parseAccessDeclaration<TValue>(
    state: AccessDeclarationArgs | null,
    declaration: Partial<Record<AccessDeclaration, TValue>>
): {
    accessDeclaration: AccessDeclaration
    value: TValue
    specificity: number
} | null {
    const debug = false

    if (state === null) return null
    const matches: Array<{
        accessDeclaration: AccessDeclaration
        value: TValue
        specificity: number
    }> = []

    for (const [key, value] of Object.entries(declaration)) {
        const [period, signupState, exhibitorStatus] = key.split(":::")
        if (
            (period === "*" || period === state.period) &&
            isSignupStateMatched(
                state.signupState,
                signupState as SignupState
            ) &&
            (exhibitorStatus === "*" ||
                exhibitorStatus === state.exhibitorStatus)
        ) {
            matches.push({
                accessDeclaration: key as AccessDeclaration,
                value,
                specificity: accessDeclarationSpecificity(
                    key as AccessDeclaration
                )
            })
        }
    }

    if (matches.length === 0) return null

    const sortedMatches = matches.sort((a, b) => b.specificity - a.specificity)

    if (debug && import.meta.env.MODE === "development") {
        console.log(`[DEBUG Access Declaration]: Picked`, sortedMatches[0])
        console.table(matches)
    }
    return sortedMatches[0]
}

export function isSignupStateMatched(
    signupState: SignupState,
    min: SignupState | "*"
): boolean {
    if (min === "*") return true
    const values: Record<SignupState, number> = {
        unsigned: 0,
        ir_signed: 1,
        cr_signed: 2
    }

    return values[signupState] >= values[min]
}

export function accessDeclarationSpecificity(
    declaration: AccessDeclaration
): number {
    return declaration
        .split(":::")
        .map(part => (part === "*" ? 0 : 1))
        .reduce<number>((a, b) => a + b, 0)
}
