import { parseAccessDeclaration } from "@/forms/access_declaration_logic"
import IrRegistrationPage from "@/forms/ir_signup/ir_registration.page"
import { getExhibitorStatus } from "@/shared/hooks/api/useAccessDeclaration"
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
                        period: dashboard.period,
                        signupState: getExhibitorStatus(
                            dashboard.has_signed_ir,
                            dashboard.has_signed_fr
                        )
                    },
                    {
                        "initial_registration:::ir_signed:::*": true,
                        "complete_registration:::ir_signed:::*": true,
                        "complete_registration:::cr_signed:::*": true,
                        "after_complete_registration:::cr_signed:::*": true
                    }
                )
        }
    ]
} as const satisfies Form
