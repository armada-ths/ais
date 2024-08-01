import { parseAccessDeclaration } from "@/forms/access_declaration_logic"
import IrRegistrationPage from "@/forms/ir_signup/ir_registration.page"
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
                !!parseAccessDeclaration(
                    {
                        exhibitorStatus: dashboard.application_status,
                        period: dashboard.period
                    },
                    {
                        "*:::!unsigned_ir": true
                    }
                )
        }
    ]
} as const satisfies Form
