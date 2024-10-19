import { AccessDeclarationArgs } from "@/forms/access_declaration_logic"
import {
    DashboardResponse,
    SigningStep,
    useDashboard
} from "@/shared/hooks/api/useDashboard"

export function getSigningStep(data: DashboardResponse) {
    if (data?.ir_signature != null && data.cr_signature != null) {
        return SigningStep.SIGNED_CR
    } else if (data?.ir_signature != null) {
        return SigningStep.SIGNED_IR
    }
    return SigningStep.UNSIGNED_IR
}

export function useAccessDeclaration(): AccessDeclarationArgs | null {
    const { data } = useDashboard()

    if (data == null) return null

    return {
        period: data.period,
        applicationStatus: data.application_status,
        signingStep: getSigningStep(data)
    }
}
