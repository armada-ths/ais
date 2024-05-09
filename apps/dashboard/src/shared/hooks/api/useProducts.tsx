import { useDashboard } from "@/shared/hooks/api/useDashboard"

/**
 * All available products that can be purchased
 * by the companies
 */
export function useProducts() {
    const { data, ...rest } = useDashboard()
    return {
        data: data?.products,
        ...rest
    }
}
