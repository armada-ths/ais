import IrRegistrationPage from "@/forms/ir_signup/ir_registration.page"
import { Form } from "../form_types"

export const form: Form = {
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
            isDone: ({ registration }) =>
                [
                    "initial_registration_signed",
                    "complete_registration_ir_signed",
                    "complete_registration_signed"
                ].includes(registration.type)
        }
    ]
}
