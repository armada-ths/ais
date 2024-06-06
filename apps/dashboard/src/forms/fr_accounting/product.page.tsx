import {
    Card,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger
} from "@/components/ui/tooltip"
import {
    belongsToSection,
    getProductWithAdjustedPrice
} from "@/forms/fr_accounting/accounting_utilities"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { RegistrationSection } from "@/shared/vars"
import { InputText } from "primereact/inputtext"
import React, { useMemo } from "react"
import { useDispatch } from "react-redux"
import {
    Category,
    Product,
    pickProduct,
    unpickProduct
} from "../../store/products/products_slice"
import { cx } from "../../utils/cx"
import { formatCurrency } from "../../utils/format_currency"
import { FormWrapper } from "../FormWrapper"

function InputCard({ product }: { product: Product }) {
    const dispatch = useDispatch()
    const { data: orders } = useOrders()
    const { data: products } = useProducts()
    const order = orders.find(x => x.product.id === product.id)
    const productWithAdjustedPrice = getProductWithAdjustedPrice(
        product.id,
        orders,
        products
    )
    const productAdjustedUnitPrice =
        (productWithAdjustedPrice?.adjustedPrice ?? 0) / (order?.quantity ?? 1)

    const selected = orders.find(x => x.product.id === product.id)

    const productPackage = getProductWithAdjustedPrice(
        order?.product.id,
        orders,
        products
    )

    const packageProductBaseQuantity =
        productPackage?.child_products?.find(
            current => current.child_product.id === product.id
        )?.quantity ?? 0

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
        <Card
            className={cx("w-full", {
                "border-2 border-emerald-500": selected
            })}
        >
            <CardHeader className="flex flex-row justify-between">
                <div className="">
                    <CardTitle className="text-xl">
                        {product.short_name || product.name}
                    </CardTitle>
                    <CardDescription>{product.description}</CardDescription>
                </div>
                <div className="!mt-0 flex flex-1 items-start justify-end">
                    {product.max_quantity <= 1 ? (
                        <Tooltip>
                            <TooltipTrigger>
                                <Switch
                                    onChange={() =>
                                        onChange(selected == null ? 1 : 0)
                                    }
                                    checked={
                                        selected != null ||
                                        packageProductBaseQuantity > 0
                                    }
                                    disabled={packageProductBaseQuantity > 0}
                                />
                            </TooltipTrigger>
                            <TooltipContent
                                hidden={packageProductBaseQuantity <= 0}
                            >
                                Included in package
                            </TooltipContent>
                        </Tooltip>
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
            </CardHeader>
            <CardFooter>
                {selected != null && selected.quantity > 1 && (
                    <div className="mb-1 inline-flex">
                        <p className="rounded bg-gray-400 p-1 px-3 text-sm text-white">
                            Unit price{" "}
                            {formatCurrency(productAdjustedUnitPrice)} kr
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
                            : `${formatCurrency(
                                  productWithAdjustedPrice?.adjustedPrice ?? NaN
                              )} kr`}
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
            </CardFooter>
        </Card>
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

export function ProductFormPage({ section }: { section: RegistrationSection }) {
    const { data: allProducts } = useProducts()
    const products = allProducts.filter(product =>
        belongsToSection(product, section)
    )

    console.log("PRODUCTS", products, allProducts)

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

    const description = allProducts[0]?.registration_section?.description

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
                <div className="flex w-[450px] flex-col gap-10">
                    {categorizedProducts.map(([section, categoryProducts]) => (
                        <React.Fragment key={section}>
                            {categoryProducts.products.length > 0 && (
                                <div className="flex w-full flex-col gap-5">
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
