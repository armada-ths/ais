import { useDashboard } from "@/shared/hooks/api/useDashboard"

export function useAccessDeclaration() {
    const { data, ...rest } = useDashboard()

    if (data == null) {
        return {
            data: null,
            ...rest
        }
    }

    const period = data.period
    const exhibitorStatus = data.application_status

    if (period == null) {
        return {
            data: null,
            ...rest
        }
    }

    const state = {
        period,
        exhibitorStatus
    }

    return {
        data: state,
        ...rest
    }
}
