import { SignupState } from "@/forms/access_declaration_logic"
import { useDashboard } from "@/shared/hooks/api/useDashboard"

export function getExhibitorStatus(
    hasSignedIr?: boolean,
    hasSignedCr?: boolean
) {
    if (hasSignedCr) {
        return SignupState.CrSigned
    } else if (hasSignedIr) {
        return SignupState.IrSigned
    }
    return SignupState.Unsigned
}

export function useAccessDeclaration() {
    const { data, ...rest } = useDashboard()

    const period = data?.period
    const signupState = getExhibitorStatus(
        data?.has_signed_ir,
        data?.has_signed_fr
    )
    const exhibitorStatus = data?.application_status

    if (period == null || signupState == null || exhibitorStatus == null) {
        return {
            data: null,
            ...rest
        }
    }

    const state = {
        period,
        signupState,
        exhibitorStatus
    }

    return {
        data: state,
        ...rest
    }
}
