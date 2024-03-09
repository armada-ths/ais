import {
    selectAdjustedProductPrice,
    selectProductPackage,
    selectProductsSelectedWithoutPackagesWithAdjustedPrice
} from "@/store/products/products_selectors"
import { RootState } from "@/store/store"
import { formatCurrency } from "@/utils/format_currency"
import { useSelector } from "react-redux"
import ProductCard from "./ProductCard"

export function FormSidebarCartSummary() {
    const productPackage = useSelector(selectProductPackage)
    const selectedProducts = useSelector(
        selectProductsSelectedWithoutPackagesWithAdjustedPrice
    )
    const packagePrice = useSelector((state: RootState) =>
        productPackage == null
            ? undefined
            : selectAdjustedProductPrice(state, productPackage?.id)
    )

    const totalPrice =
        selectedProducts.reduce((acc, current) => acc + current.price, 0) +
        (productPackage?.unit_price ?? 0)

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
                                    {productPackage.child_products.map(
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
                                            packagePrice ??
                                                productPackage.unit_price
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
                        {selectedProducts
                            .filter(
                                current =>
                                    current.price >= 0 && current.category
                            )
                            .map(current => (
                                <ProductCard
                                    key={current.id}
                                    product={current}
                                />
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
