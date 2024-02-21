import { useDispatch, useSelector } from "react-redux"
import { FormWrapper } from "../FormWrapper"
import {
    selectAdjustedProductPrice,
    selectProductPackage,
    selectPackageBaseProductQuantity,
    selectSelectedProduct,
    selectUnitAdjustedProductPrice
} from "../../store/products/products_selectors"
import {
    Category,
    Product,
    pickProduct,
    unpickProduct
} from "../../store/products/products_slice"
import { InputText } from "primereact/inputtext"
import { RootState } from "../../store/store"
import { InputSwitch } from "primereact/inputswitch"
import { cx } from "../../utils/cx"
import React, { useMemo } from "react"
import { formatCurrency } from "../../utils/format_currency"

function InputCard({ product }: { product: Product }) {
    const dispatch = useDispatch()
    const selected = useSelector((state: RootState) =>
        selectSelectedProduct(state, product.id)
    )
    const adjustedUnitPrize = useSelector((state: RootState) =>
        selectUnitAdjustedProductPrice(state, product.id)
    )
    const adjustedPrize = useSelector((state: RootState) =>
        selectAdjustedProductPrice(state, product.id)
    )
    const productPackage = useSelector(selectProductPackage)
    const packageProductBaseQuantity = useSelector((state: RootState) =>
        selectPackageBaseProductQuantity(state, product.id)
    )

    function onChange(quantity: number) {
        if (isNaN(quantity)) quantity = 0
        if (product.max_quantity != null && quantity > product.max_quantity)
            quantity = product.max_quantity
        if (quantity <= 0 || quantity == null) {
            dispatch(
                unpickProduct({
                    id: product.id
                })
            )
        } else {
            if (
                product.max_quantity != null &&
                product.max_quantity <= 1 &&
                packageProductBaseQuantity > 0
            ) {
                return
            }

            dispatch(
                pickProduct({
                    id: product.id,
                    quantity,
                    isPackage: false
                })
            )
        }
    }

    const packageName =
        productPackage?.short_name || productPackage?.name || "package"

    return (
        <div
            className={cx(
                "w-full rounded bg-white p-5 shadow-sm",
                selected && "border-2 border-emerald-500"
            )}
        >
            <div className="flex justify-between gap-10">
                <div className="w-3/4">
                    <p className="text text-slate-700">
                        {product.short_name || product.name}
                    </p>
                    <p className="text-xs text-slate-500">
                        {product.description}
                    </p>
                </div>
                <div className="flex items-center justify-center">
                    {product.max_quantity <= 1 ? (
                        <InputSwitch
                            onChange={() => onChange(selected == null ? 1 : 0)}
                            checked={
                                selected != null ||
                                packageProductBaseQuantity > 0
                            }
                            disabled={packageProductBaseQuantity > 0}
                            tooltip={
                                packageProductBaseQuantity > 0
                                    ? "Included in package"
                                    : undefined
                            }
                            tooltipOptions={{
                                showOnDisabled: true
                            }}
                        />
                    ) : (
                        <InputText
                            placeholder="Quantity"
                            className="w-40"
                            value={selected?.quantity.toString() ?? "0"}
                            min={0}
                            max={product.max_quantity}
                            type="number"
                            onChange={event =>
                                onChange(parseInt(event.target.value))
                            }
                        />
                    )}
                </div>
            </div>
            <div className="mt-5">
                {selected != null && selected.quantity > 1 && (
                    <div className="mb-1 inline-flex">
                        <p className="rounded bg-gray-400 p-1 px-3 text-sm text-white">
                            Unit price {formatCurrency(adjustedUnitPrize)} kr
                        </p>
                    </div>
                )}
                <div className="flex items-center gap-3">
                    <p className="rounded bg-emerald-400 p-1 px-3 text-lg text-white">
                        {product.max_quantity <= 1 &&
                        packageProductBaseQuantity > 0
                            ? `Included In ${packageName}`
                            : packageProductBaseQuantity > 0 &&
                              (selected?.quantity ?? 0) <= 0
                            ? "0 kr"
                            : `${formatCurrency(adjustedPrize)} kr`}
                    </p>
                    {product.max_quantity > 1 &&
                        packageProductBaseQuantity > 0 && (
                            <>
                                <p className="text-slate-500">in addition to</p>
                                <p className="rounded bg-emerald-400 p-1 px-3 text-sm text-white">
                                    {packageProductBaseQuantity} included in{" "}
                                    {packageName}
                                </p>
                            </>
                        )}
                </div>
            </div>
        </div>
    )
}

export function DiscountCard({ product }: { product: Product }) {
    return (
        <div className="flex items-center justify-center">
            <div className="w-full rounded bg-gradient-to-r from-yellow-500 to-yellow-300 p-1">
                <div className="flex h-full w-full bg-white p-5">
                    <div className="flex-[2]">
                        <h3 className="bg-white text-lg text-yellow-600">
                            {product.short_name || product.name}
                        </h3>
                        <p className="text-xs text-yellow-800">
                            {product.description}
                        </p>
                    </div>
                    <div className="flex flex-1 items-center justify-center">
                        <p className="rounded bg-gradient-to-br from-yellow-600 to-yellow-500 p-2 px-4 font-bold text-white">
                            {formatCurrency(product.unit_price)} kr
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export function ProductFormPage({
    selector
}: {
    selector: (state: RootState) => Product[]
}) {
    const products = useSelector(selector)
    const categorizedProducts = useMemo(
        () =>
            Object.entries(
                products.reduce<
                    Record<string, { category?: Category; products: Product[] }>
                >(
                    // Split products into categories
                    (total, current) => {
                        if (current.category == null) {
                            total["none"].products.push(current)
                            return total
                        }

                        const target = total[current.category.name]
                        if (target == null)
                            total[current.category.name] = {
                                category: current.category,
                                products: [current]
                            }
                        else target.products.push(current)

                        return total
                    },
                    { none: { products: [] } }
                )
            ),
        [products]
    )

    const description = products[0]?.registration_section?.description

    return (
        <>
            {description && (
                <div className="flex w-full justify-center">
                    <div className="w-[450px] rounded bg-slate-200 p-2 px-4">
                        <p className="text-slate-600">{description}</p>
                    </div>
                </div>
            )}
            <FormWrapper>
                <div className="flex flex-col gap-10">
                    {categorizedProducts.map(([section, categoryProducts]) => (
                        <React.Fragment key={section}>
                            {categoryProducts.products.length > 0 && (
                                <div className="flex flex-col gap-5">
                                    <div>
                                        {section !== "none" && (
                                            <h3 className="text-xl text-emerald-400">
                                                {section}
                                            </h3>
                                        )}
                                        <p className="mt-1 text-sm text-slate-500">
                                            {
                                                categoryProducts.category
                                                    ?.description
                                            }
                                        </p>
                                    </div>

                                    {categoryProducts.products
                                        .filter(
                                            current => current.unit_price < 0
                                        )
                                        .map(current => (
                                            <DiscountCard
                                                key={current.id}
                                                product={current}
                                            />
                                        ))}

                                    {categoryProducts.products
                                        .filter(
                                            current => current.unit_price >= 0
                                        )
                                        .map(current => (
                                            <InputCard
                                                key={current.id}
                                                product={current}
                                            />
                                        ))}
                                </div>
                            )}
                        </React.Fragment>
                    ))}
                </div>
            </FormWrapper>
        </>
    )
}
