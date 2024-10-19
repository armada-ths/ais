import { parseAccessDeclaration } from "@/forms/access_declaration_logic"
import {
    ApplicationStatus,
    RegistrationPeriod,
    SigningStep
} from "@/shared/hooks/api/useDashboard"
import { describe, expect, it } from "vitest"

describe(parseAccessDeclaration.name, () => {
    it("picks right privilege from trivial case", () => {
        const result = parseAccessDeclaration(
            {
                applicationStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signingStep: SigningStep.SIGNED_CR
            },
            {
                "before_initial_registration:::unsigned_ir:::pending": 0,
                "initial_registration:::signed_cr:::accepted": 1,
                "between_ir_and_cr:::signed_ir:::waitlist": 2
            }
        )

        expect(result).toBeDefined()
        expect(result?.value).toBe(1)
        expect(result).toMatchObject({
            accessDeclaration: "initial_registration:::signed_cr:::accepted"
        })
    })
    it("picks declaration with highest priority (first match)", () => {
        const result = parseAccessDeclaration(
            {
                applicationStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signingStep: SigningStep.SIGNED_CR
            },
            {
                "*:::*:::*": 0,
                "initial_registration:::signed_cr:::*": 1,
                "initial_registration:::signed_cr:::accepted": 2
            }
        )

        expect(result).toBeDefined()
        expect(result?.value).toBe(0)
        expect(result).toMatchObject({
            accessDeclaration: "*:::*:::*"
        })
        const result2 = parseAccessDeclaration(
            {
                applicationStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signingStep: SigningStep.SIGNED_CR
            },
            {
                "initial_registration:::signed_cr:::accepted": 2,
                "initial_registration:::signed_cr:::*": 1,
                "*:::*:::*": 0
            }
        )

        expect(result2).toBeDefined()
        expect(result2?.value).toBe(2)
        expect(result2).toMatchObject({
            accessDeclaration: "initial_registration:::signed_cr:::accepted"
        })

        const backwardsResult = parseAccessDeclaration(
            {
                applicationStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signingStep: SigningStep.SIGNED_CR
            },
            {
                "initial_registration:::signed_cr:::accepted": 2,
                "initial_registration:::signed_cr:::*": 1,
                "*:::*:::*": 0
            }
        )

        expect(backwardsResult).toBeDefined()
        expect(backwardsResult?.value).toBe(2)
        expect(backwardsResult).toMatchObject({
            accessDeclaration: "initial_registration:::signed_cr:::accepted"
        })
    })

    it("uses wildcard when no match", () => {
        const result = parseAccessDeclaration(
            {
                applicationStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signingStep: SigningStep.SIGNED_IR
            },
            {
                "*:::*:::*": 0,
                "initial_registration:::signed_cr:::*": 1
            }
        )

        expect(result).toBeDefined()
        expect(result?.value).toBe(0)
    })

    it("returns null when no match", () => {
        const result = parseAccessDeclaration(
            {
                applicationStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signingStep: SigningStep.SIGNED_IR
            },
            {
                "initial_registration:::signed_cr:::*": 1
            }
        )

        expect(result).toBeNull()

        expect(
            parseAccessDeclaration(null, {
                "initial_registration:::signed_cr:::*": 1
            })
        ).toBeNull()
    })
})
