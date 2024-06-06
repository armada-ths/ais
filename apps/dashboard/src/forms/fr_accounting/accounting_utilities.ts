import { DashboardResponse } from "@/shared/hooks/api/useDashboard"

/**
 * Get the price by checking discount and quantity
 * If no discount exists, return the unit price of
 * the product
 */
export function getAdjustedProductPrice(
    productId: number,
    orders: DashboardResponse["orders"],
    products: DashboardResponse["products"]
) {
    const product = products.find(x => x.id === productId)
    const order = orders.find(x => x.product.id === productId)
    return (
        (order?.quantity ?? 1) * (order?.unit_price ?? product?.unit_price ?? 0)
    )
}
