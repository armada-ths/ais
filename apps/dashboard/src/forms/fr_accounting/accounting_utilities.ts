import { DashboardResponse } from "@/shared/hooks/api/useDashboard"
import {
    EVENTS_REGISTRATION_SECTION_KEY,
    EXTRAS_REGISTRATION_SECTION_KEY,
    PACKAGE_SECTION_KEY
} from "@/shared/vars"

/**
 * Get the price by checking discount and quantity
 * If no discount exists, return the unit price of
 * the product
 */
export function getProductsWithAdjustedPrice(
    orders: DashboardResponse["orders"],
    products: DashboardResponse["products"]
) {
    return products.map(product => {
        const order = orders.find(x => x.product.id === product.id)
        return {
            ...product,
            adjustedPrice:
                (order?.quantity ?? 1) *
                (order?.unit_price ?? product?.unit_price ?? 0)
        }
    })
}
export function getProductWithAdjustedPrice(
    productId: number | undefined,
    orders: DashboardResponse["orders"],
    products: DashboardResponse["products"]
) {
    if (productId == null) return null
    const order = orders.find(x => x.product.id === productId)

    const product = products.find(x => x.id === productId)
    return {
        ...product,
        adjustedPrice:
            (order?.quantity ?? 1) *
            (order?.unit_price ?? product?.unit_price ?? 0)
    }
}

export function belongsToSection(
    product: DashboardResponse["products"][0],
    section:
        | typeof PACKAGE_SECTION_KEY
        | typeof EXTRAS_REGISTRATION_SECTION_KEY
        | typeof EVENTS_REGISTRATION_SECTION_KEY
) {
    return product.registration_section?.name === section
}
