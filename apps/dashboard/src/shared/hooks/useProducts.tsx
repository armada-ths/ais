import { useDashboard } from "@/shared/hooks/useDashboard"

export function useProducts() {
    const { data, ...rest } = useDashboard()
    return {
        data: data?.products,
        ...rest
    }
}
