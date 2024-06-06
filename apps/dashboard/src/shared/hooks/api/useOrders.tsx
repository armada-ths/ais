import { useDashboard } from "@/shared/hooks/api/useDashboard"

/**
 * All available products that can be purchased
 * by the companies
 */
export function useOrders() {
    const { data, ...rest } = useDashboard()
    return {
        data: data?.orders ?? [],
        ...rest
    }
}
