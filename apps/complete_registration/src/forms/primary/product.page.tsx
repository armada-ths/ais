import { useDispatch, useSelector } from "react-redux"
import { FormWrapper } from "../FormWrapper"
import { selectSelectedProduct } from "../../store/products/products_selectors"
import {
    EVENTS_REGISTRATION_SECTION_KEY,
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

    function onChange(quantity: number) {
        if (isNaN(quantity)) return
        if (quantity <= 0 || quantity == null) {
            dispatch(
                unpickProduct({
                    id: product.id
                })
            )
        } else {
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
                    <p className="text">{product.name}</p>
                    <p className="text-sm">{product.description}</p>
                </div>
                <div className="flex items-center justify-center">
                    {product.max_quantity <= 1 ? (
                        <InputSwitch
                            onChange={() => onChange(selected == null ? 1 : 0)}
                            checked={selected != null}
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
