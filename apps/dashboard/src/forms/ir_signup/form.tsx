import IrRegistrationPage from "@/forms/ir_signup/ir_registration.page"
import { RegistrationStatus } from "@/store/company/company_slice"
import { Form } from "../form_types"

export const form = {
    key: "ir_signup",
    name: "Initial Registration",
    description: "Signup to become an exhibitor for Armada",
    pages: [
        {
            id: "sign_ir",
            title: "Sign up for Armada",
            pageComponent: IrRegistrationPage,
            fields: [],
            hasNextButton: false,
            isDone: ({ dashboard }) =>
                (
                    [
                        "initial_registration_signed",
                        "complete_registration_ir_signed",
                        "complete_registration_signed",
                        "after_initial_registration_signed",
                        "complete_registration_ir_signed"
                    ] as RegistrationStatus[]
                ).includes(dashboard.type)
        }
    ]
} as const satisfies Form
