import { useDispatch, useSelector } from "react-redux"
import { FormWrapper } from "../FormWrapper"
import {
    selectAdjustedProductPrice,
    selectProductPackage,
    selectPackageBaseProductQuantity,
    selectSelectedProduct
} from "../../store/products/products_selectors"
import {
    Product,
    pickProduct,
    unpickProduct
} from "../../store/products/products_slice"
import { InputText } from "primereact/inputtext"
import { RootState } from "../../store/store"
import { InputSwitch } from "primereact/inputswitch"
import { cx } from "../../utils/cx"
import React, { useMemo } from "react"

function InputCard({ product }: { product: Product }) {
    const dispatch = useDispatch()
    const selected = useSelector((state: RootState) =>
        selectSelectedProduct(state, product.id)
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
        if (quantity > product.max_quantity) quantity = product.max_quantity
        if (quantity <= 0 || quantity == null) {
            dispatch(
                unpickProduct({
                    id: product.id
                })
            )
        } else {
            if (product.max_quantity <= 1 && packageProductBaseQuantity > 0)
                return

            dispatch(
                pickProduct({
                    id: product.id,
                    quantity,
                    isPackage: false
                })
            )
        }
    }

    return (
        <div
            className={cx(
                "w-full rounded bg-white p-5 shadow-sm",
                selected && "border-2 border-emerald-500"
            )}
        >
            <div className="flex justify-between gap-10">
                <div className="w-3/4">
                    <p className="text text-slate-700">{product.name}</p>
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
                <div className="flex items-center gap-3">
                    <p className="rounded bg-emerald-400 p-1 px-3 text-lg text-white">
                        {product.max_quantity <= 1 &&
                        packageProductBaseQuantity > 0
                            ? `Included In ${productPackage?.name ?? "Package"}`
                            : `${Intl.NumberFormat("sv").format(
                                  adjustedPrize
                              )} kr`}
                    </p>
                    {product.max_quantity > 1 &&
                        packageProductBaseQuantity > 0 && (
                            <>
                                <p className="text-slate-500">in addition to</p>
                                <p className="rounded bg-emerald-400 p-1 px-3 text-sm text-white">
                                    {packageProductBaseQuantity} included in{" "}
                                    {productPackage?.name ?? "package"}
                                </p>
                            </>
                        )}
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
    const compartmentalizedProducts = useMemo(
        () =>
            Object.entries(
                products.reduce<Record<string, Product[]>>(
                    // Split products into categories
                    (total, current) => {
                        if (current.category == null) {
                            total["none"].push(current)
                            return total
                        }

                        const target = total[current.category.name]
                        if (target == null)
                            total[current.category.name] = [current]
                        else target.push(current)

                        return total
                    },
                    { none: [] }
                )
            ),
        [products]
    )

    return (
        <FormWrapper>
            <div className="flex flex-col gap-10">
                {compartmentalizedProducts.map(([section, products]) => (
                    <React.Fragment key={section}>
                        {products.length > 0 && (
                            <div className="flex flex-col gap-5">
                                {section !== "none" && (
                                    <h3 className="text-xl text-emerald-400">
                                        {section}
                                    </h3>
                                )}

                                {products.map(current => (
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
    )
}
