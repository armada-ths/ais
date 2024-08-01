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
    priority: number
} | null {
    const debug = false

    if (state === null) return null
    const matches: Array<{
        accessDeclaration: AccessDeclaration
        value: TValue
        priority: number
    }> = []

    for (const [i, [key, value]] of Object.entries(declaration).entries()) {
        const [period, exhibitorStatus] = key.split(":::")

        if (
            accessPropertyMatches(state.period, period) &&
            accessPropertyMatches(state.exhibitorStatus, exhibitorStatus)
        ) {
            matches.push({
                accessDeclaration: key as AccessDeclaration,
                value,
                priority: i
            })
        }
    }

    if (matches.length === 0) return null

    const sortedMatches = matches.sort((a, b) => a.priority - b.priority)

    if (debug && import.meta.env.MODE === "development") {
        console.log(`[DEBUG Access Declaration]: Picked`, sortedMatches[0])
        console.table(matches)
    }

    console.log({ state, sortedMatches })

    return sortedMatches[0]
}