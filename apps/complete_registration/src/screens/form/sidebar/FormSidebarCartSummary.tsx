import { useSelector } from "react-redux"
import {
    selectProductPackage,
    selectProductsSelectedWithoutPackages
} from "../../../store/products/products_selectors"
import { Card } from "./PageCard"

export function FormSidebarCartSummary() {
    const productPackage = useSelector(selectProductPackage)
    const selectedProducts = useSelector(selectProductsSelectedWithoutPackages)

    return (
        <div className="relative h-full">
            <div className="sticky top-0 flex flex-col gap-y-2">
                <div className="max-h-full overflow-auto p-5">
                    {productPackage != null && (
                        <div className="mb-5 rounded bg-emerald-400 p-5 py-3">
                            <div className="mb-5 flex flex-wrap items-center justify-between gap-x-4">
                                <h3 className="text-xl text-white">Package</h3>
                                <h4 className="mt-1 inline-block rounded bg-white p-1 px-3 text-emerald-400">
                                    {productPackage.name}
                                </h4>
                            </div>
                            <div>
                                <h4 className="text-white">
                                    Included in package
                                </h4>
                                <ul className="ml-4 list-disc text-white">
                                    {productPackage.child_products.map(
                                        ({ child_product, quantity }) => (
                                            <li
                                                key={child_product.id}
                                                className="flex"
                                            >
                                                <p>{child_product.name}</p>
                                                {quantity > 1 && (
                                                    <p> x {quantity}</p>
                                                )}
                                            </li>
                                        )
                                    )}
                                </ul>
                                <div>
                                    <h4 className="mt-5 rounded bg-white p-1 px-3 text-center text-emerald-400">
                                        {productPackage.unit_price} kr
                                    </h4>
                                </div>
                            </div>
                        </div>
                    )}
                    <div className="flex flex-col gap-y-2">
                        <h2 className="mb-2 text-center text-xl">
                            Selected products
                        </h2>
                        {selectedProducts.map(current => (
                            <Card key={current.id} className="">
                                <p className="">{current.name}</p>
                                <p className="mt-2 text-slate-400">
                                    {current.unit_price} kr
                                </p>
                            </Card>
                        ))}
                    </div>
                    <div className="flex-1" />
                    <div className="mt-5 flex items-center justify-between rounded bg-slate-200 p-1 px-3">
                        <h2 className="text-lg">Total</h2>
                        <p className="text font-bold">
                            {selectedProducts.reduce(
                                (acc, current) => acc + current.unit_price,
                                0
                            ) + (productPackage?.unit_price ?? 0)}{" "}
                            kr
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
