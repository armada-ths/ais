import { AccessDeclarationArgs } from "@/forms/access_declaration_logic"
import { useDashboard } from "@/shared/hooks/api/useDashboard"

export function useAccessDeclaration(): AccessDeclarationArgs | null {
    const { data } = useDashboard()

    if (data?.period == null) {
        return null
    }

    return {
        period: data.period,
        exhibitorStatus: data.application_status
    }
}
