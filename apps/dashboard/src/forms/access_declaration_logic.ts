import {
    ApplicationStatus,
    RegistrationPeriod
} from "@/shared/hooks/api/useDashboard"

export type AccessDeclaration = `${RegistrationPeriod | "*"}:::${
    | (ApplicationStatus | `!${ApplicationStatus}`)
    | "*"}`

export interface AccessDeclarationArgs {
    period: RegistrationPeriod
    exhibitorStatus: ApplicationStatus | "unsigned_ir"
}

function accessPropertyMatches(variable: string, property: string): boolean {
    if (property === "*") return true
    if (property.startsWith("!")) {
        return variable !== property.slice(1)
    }
    return variable === property
}

export function parseAccessDeclaration<TValue>(
    state: AccessDeclarationArgs | null,
    declaration: Partial<Record<AccessDeclaration, TValue>>
): {
    accessDeclaration: AccessDeclaration
    value: TValue
} | null {
    const debug = false

    if (state === null) return null
    const matches: Array<{
        accessDeclaration: AccessDeclaration
        value: TValue
        priority: number
    }> = []

    for (const [key, value] of Object.entries(declaration)) {
        const [period, exhibitorStatus] = key.split(":::")

        if (
            accessPropertyMatches(state.period, period) &&
            accessPropertyMatches(state.exhibitorStatus, exhibitorStatus)
        ) {
            const result = {
                accessDeclaration: key as AccessDeclaration,
                value
            }

            if (debug && import.meta.env.MODE === "development") {
                console.log(`[DEBUG Access Declaration]: Picked`, result)
                console.table(matches)
            }

            return result
        }
    }

    return null
}

export function checkAccessDeclarations(
    state: AccessDeclarationArgs | null,
    declarations: AccessDeclaration[]
) {
    const declarationObject = declarations.reduce<
        Partial<Record<AccessDeclaration, boolean>>
    >((acc, declaration) => {
        acc[declaration] = true
        return acc
    }, {})
    return parseAccessDeclaration(state, declarationObject)?.value ?? false
}
