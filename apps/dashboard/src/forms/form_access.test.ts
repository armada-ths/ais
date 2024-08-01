// import { SignupState } from "@/forms/access_declaration_logic"
// import { CardStatus, isFormOpen } from "@/forms/form_access"
// import {
//     ApplicationStatus,
//     RegistrationPeriod
// } from "@/shared/hooks/api/useDashboard"
// import { describe, expect, it } from "vitest"

// describe(isFormOpen.name, () => {
//     it("should return true if the form is open", () => {
//         expect(
//             isFormOpen(
//                 {
//                     period: RegistrationPeriod.InitialRegistration,
//                     signupState: SignupState.CrSigned,
//                     exhibitorStatus: ApplicationStatus.ACCEPTED
//                 },
//                 "ir_signup",
//                 {
//                     ir_signup: {
//                         "initial_registration:::unsigned:::*": CardStatus.Shown
//                     },
//                     ir_additional_info: {},
//                     core_values: {},
//                     exhibitor_catalog: {},
//                     fr_accounting: {},
//                     receipt: {},
//                     transport: {},
//                     sture: {}
//                 }
//             )
//         ).toBe(true)
//         expect(
//             isFormOpen(
//                 {
//                     period: RegistrationPeriod.InitialRegistration,
//                     signupState: SignupState.CrSigned,
//                     exhibitorStatus: ApplicationStatus.ACCEPTED
//                 },
//                 "ir_signup",
//                 {
//                     ir_signup: {
//                         "*:::*:::*": CardStatus.Shown
//                     },
//                     ir_additional_info: {},
//                     core_values: {},
//                     exhibitor_catalog: {},
//                     fr_accounting: {},
//                     receipt: {},
//                     transport: {},
//                     sture: {}
//                 }
//             )
//         ).toBe(true)
//     })

//     it("should return false if the form is locked", () => {
//         expect(
//             isFormOpen(
//                 {
//                     period: RegistrationPeriod.InitialRegistration,
//                     signupState: SignupState.CrSigned,
//                     exhibitorStatus: ApplicationStatus.ACCEPTED
//                 },
//                 "ir_signup",
//                 {
//                     ir_signup: {
//                         "*:::*:::*": CardStatus.HiddenLocked
//                     },
//                     ir_additional_info: {},
//                     core_values: {},
//                     exhibitor_catalog: {},
//                     fr_accounting: {},
//                     receipt: {},
//                     transport: {},
//                     sture: {}
//                 }
//             )
//         ).toBe(false)
//         expect(
//             isFormOpen(
//                 {
//                     period: RegistrationPeriod.InitialRegistration,
//                     signupState: SignupState.CrSigned,
//                     exhibitorStatus: ApplicationStatus.ACCEPTED
//                 },
//                 "ir_signup",
//                 {
//                     ir_signup: {},
//                     ir_additional_info: {},
//                     core_values: {},
//                     exhibitor_catalog: {},
//                     fr_accounting: {},
//                     receipt: {},
//                     transport: {},
//                     sture: {}
//                 }
//             )
//         ).toBe(false)
//     })

//     it("picks correct order with same specificity", () => {
//         expect(
//             isFormOpen(
//                 {
//                     period: RegistrationPeriod.CompleteRegistration,
//                     signupState: SignupState.IrSigned,
//                     exhibitorStatus: ApplicationStatus.ACCEPTED
//                 },
//                 "fr_accounting",
//                 {
//                     ir_signup: {},
//                     ir_additional_info: {},
//                     core_values: {},
//                     exhibitor_catalog: {},
//                     fr_accounting: {
//                         "complete_registration:::*:::*": CardStatus.Shown,
//                         "complete_registration:::*:::rejected":
//                             CardStatus.HiddenLocked,
//                         "complete_registration:::cr_signed:::*":
//                             CardStatus.HiddenLocked
//                     },
//                     receipt: {},
//                     transport: {},
//                     sture: {}
//                 }
//             )
//         ).toBe(true)
//     })
// })
