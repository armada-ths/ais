import {
    AccessDeclaration,
    accessDeclarationSpecificity,
    isSignupStateMatched,
    parseAccessDeclaration,
    SignupState
} from "@/forms/access_declaration_logic"
import {
    ApplicationStatus,
    RegistrationPeriod
} from "@/shared/hooks/api/useDashboard"
import { describe, expect, it } from "vitest"

describe(parseAccessDeclaration.name, () => {
    it("picks right privilege from trivial case", () => {
        const result = parseAccessDeclaration(
            {
                exhibitorStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signupState: SignupState.CrSigned
            },
            {
                "before_initial_registration:::unsigned:::pending": 0,
                "initial_registration:::cr_signed:::accepted": 1,
                "between_ir_and_cr:::ir_signed:::waitlist": 2
            }
        )

        expect(result).toBeDefined()
        expect(result?.value).toBe(1)
        expect(result).toMatchObject({
            accessDeclaration: "initial_registration:::cr_signed:::accepted",
            specificity: 3
        })
    })
    it("picks declaration with highest priority", () => {
        const result = parseAccessDeclaration(
            {
                exhibitorStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signupState: SignupState.CrSigned
            },
            {
                "*:::*:::*": 0,
                "initial_registration:::cr_signed:::*": 1,
                "initial_registration:::cr_signed:::accepted": 2
            }
        )

        expect(result).toBeDefined()
        expect(result?.value).toBe(2)
        expect(result).toMatchObject({
            accessDeclaration: "initial_registration:::cr_signed:::accepted",
            specificity: 3
        })

        const backwardsResult = parseAccessDeclaration(
            {
                exhibitorStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signupState: SignupState.CrSigned
            },
            {
                "initial_registration:::cr_signed:::accepted": 2,
                "initial_registration:::cr_signed:::*": 1,
                "*:::*:::*": 0
            }
        )

        expect(backwardsResult).toBeDefined()
        expect(backwardsResult?.value).toBe(2)
        expect(backwardsResult).toMatchObject({
            accessDeclaration: "initial_registration:::cr_signed:::accepted",
            specificity: 3
        })
    })

    it("uses wildcard when no match", () => {
        const result = parseAccessDeclaration(
            {
                exhibitorStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signupState: SignupState.IrSigned
            },
            {
                "*:::*:::*": 0,
                "initial_registration:::cr_signed:::*": 1
            }
        )

        expect(result).toBeDefined()
        expect(result?.value).toBe(0)
    })

    it("returns null when no match", () => {
        const result = parseAccessDeclaration(
            {
                exhibitorStatus: ApplicationStatus.ACCEPTED,
                period: RegistrationPeriod.InitialRegistration,
                signupState: SignupState.IrSigned
            },
            {
                "initial_registration:::cr_signed:::*": 1
            }
        )

        expect(result).toBeNull()

        expect(
            parseAccessDeclaration(null, {
                "initial_registration:::cr_signed:::*": 1
            })
        ).toBeNull()
    })
})

describe(isSignupStateMatched.name, () => {
    it.each([
        ["*:::*:::*", 0],
        ["*:::*:::accepted", 1],
        ["after_complete_registration:::cr_signed:::*", 2],
        ["after_complete_registration:::cr_signed:::*", 2],
        ["initial_registration:::cr_signed:::pending", 3]
    ] as [AccessDeclaration, number][])(
        "decides correct specificity",
        (accessDeclaration, correct) => {
            expect(accessDeclarationSpecificity(accessDeclaration)).toBe(
                correct
            )
        }
    )
})
