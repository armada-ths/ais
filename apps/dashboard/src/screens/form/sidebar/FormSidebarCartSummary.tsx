import {
    belongsToSection,
    getProductWithAdjustedPrice,
    getProductsWithAdjustedPrice
} from "@/forms/fr_accounting/accounting_utilities"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { PACKAGE_SECTION_KEY } from "@/shared/vars"
import { formatCurrency } from "@/utils/format_currency"
import ProductCard from "./ProductCard"

export function FormSidebarCartSummary() {
    const { data: orders } = useOrders()
    const { data: products } = useProducts()

    const packageOrder = orders.find(
        order =>
            order.product.registration_section?.name.toLowerCase() ===
            PACKAGE_SECTION_KEY.toLowerCase()
    )
    const productPackage = getProductWithAdjustedPrice(
        packageOrder?.product.id,
        orders,
        products
    )

    const productsWithAdjustedPrices = getProductsWithAdjustedPrice(
        orders,
        products,
        {
            ordersOnly: true
        }
    )

    const selectedProducts = productsWithAdjustedPrices
        .filter(x => !belongsToSection(x, PACKAGE_SECTION_KEY))
        // Free items should be listed in the package card instead
        .filter(current => current.adjustedPrice >= 0)

    const totalPrice = productsWithAdjustedPrices.reduce(
        (acc, current) => acc + current.adjustedPrice,
        0
    )

    const grossPrice = totalPrice * 1.25

    return (
        <div className="relative h-full">
            <div className="sticky top-0 flex flex-col gap-y-2">
                <div className="max-h-full overflow-auto p-5">
                    {productPackage != null && (
                        <div className="mb-5 rounded bg-emerald-400 p-5 py-3">
                            <div className="mb-5 flex flex-wrap items-center justify-between gap-x-4">
                                <h3 className="text-xl text-white">Package</h3>
                                <h4 className="mt-1 inline-block rounded bg-white p-1 px-3 text-emerald-400">
                                    {productPackage.short_name ||
                                        productPackage.name}
                                </h4>
                            </div>
                            <div>
                                <h4 className="text-white">
                                    Included in package
                                </h4>
                                <ul className="ml-4 list-inside list-disc text-white">
                                    {productPackage.child_products?.map(
                                        ({ child_product, quantity }) => (
                                            <p
                                                key={child_product.id}
                                                className="whitespace-nowrap"
                                            >
                                                *{" "}
                                                {child_product.short_name ||
                                                    child_product.name}
                                                {quantity > 1
                                                    ? ` x ${quantity}`
                                                    : ""}
                                            </p>
                                        )
                                    )}
                                </ul>
                                <div>
                                    <h4 className="mt-5 rounded bg-white p-1 px-3 text-center text-emerald-400">
                                        {formatCurrency(
                                            productPackage.adjustedPrice
                                        )}{" "}
                                        kr
                                    </h4>
                                </div>
                            </div>
                        </div>
                    )}
                    <div className="flex flex-col gap-y-2">
                        {selectedProducts.length > 0 && (
                            <h2 className="mb-2 text-center text-xl">
                                Selected products
                            </h2>
                        )}
                        {selectedProducts.map(current => (
                            <ProductCard key={current.id} product={current} />
                        ))}
                    </div>
                    <div className="flex-1" />
                    <div className="mt-5 flex flex-col items-center justify-between rounded bg-slate-200 p-1 px-3">
                        <div className="flex w-full justify-between">
                            <h2 className="text-lg">Net</h2>
                            <p className="text">
                                {formatCurrency(totalPrice)} kr
                            </p>
                        </div>
                        <div className="flex w-full justify-between">
                            <h2 className="text-lg">VAT</h2>
                            <p className="text">25%</p>
                        </div>
                        <div className="flex w-full justify-between">
                            <h2 className="text-lg">Gross</h2>
                            <p className="text font-bold">
                                {formatCurrency(Math.round(grossPrice))} kr
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
