import { Badge } from "@/components/ui/badge"
import {
    Card,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
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
import { useAccountingMutation } from "@/forms/fr_accounting/useAccounting"
import { Product, useDashboard } from "@/shared/hooks/api/useDashboard"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { RegistrationSection } from "@/shared/vars"
import { cn } from "@/utils/cx"
import { formatCurrency } from "@/utils/format_currency"
import { cx } from "class-variance-authority"

export function ProductOrderingCard({
    product
}: {
    product: Omit<Product, "child_products" | "specific_products">
}) {
    const { updateCache } = useDashboard()
    const { data: orders } = useOrders()
    const { data: products } = useProducts()

    const { setProductOrder } = useAccountingMutation({
        onSuccess: updateCache
    })

    const order = orders.find(x => x.product.id === product.id)
    const productWithAdjustedPrice = getProductWithAdjustedPrice(
        product.id,
        orders,
        products
    )
    const productAdjustedUnitPrice =
        (productWithAdjustedPrice?.adjustedPrice ?? 0) / (order?.quantity ?? 1)

    const selected = orders.find(x => x.product.id === product.id)

    const packageOrder = orders.find(order =>
        belongsToSection(order.product, RegistrationSection.Packages)
    )
    const productPackage = getProductWithAdjustedPrice(
        packageOrder?.product.id,
        orders,
        products
    )

    const packageProductBaseQuantity =
        productPackage?.child_products?.find(
            current => current.child_product.id === product.id
        )?.quantity ?? 0

    async function onChange(quantity: number) {
        if (isNaN(quantity)) quantity = 0
        if (product.max_quantity != null && quantity > product.max_quantity)
            quantity = product.max_quantity
        if (quantity <= 0 || quantity == null) {
            await setProductOrder(product.id, 0)
        } else if (
            !(
                // If the product has a max of 1 and is already
                // included, don't allow it to be added or incremented
                (
                    product.max_quantity != null &&
                    product.max_quantity <= 1 &&
                    packageProductBaseQuantity > 0
                )
            )
        ) {
            await setProductOrder(product.id, quantity)
        }
    }

    const packageName =
        productPackage?.short_name || productPackage?.name || "package"

    return (
        <Card
            className={cx("w-full border-2", {
                "border-emerald-500": selected
            })}
        >
            <CardHeader className="flex flex-col justify-between">
                <div
                    className={cn("flex", {
                        "mb-1": product.description
                    })}
                >
                    <div className="">
                        <CardTitle className="text-xl">
                            {product.short_name || product.name}
                        </CardTitle>
                    </div>
                    <div className="!mt-0 flex flex-1 items-start justify-end">
                        {product.max_quantity != null &&
                        product.max_quantity <= 1 ? (
                            packageProductBaseQuantity <= 0 ? (
                                <Switch
                                    onCheckedChange={value =>
                                        onChange(value ? 1 : 0)
                                    }
                                    checked={
                                        selected != null ||
                                        packageProductBaseQuantity > 0
                                    }
                                    disabled={packageProductBaseQuantity > 0}
                                />
                            ) : (
                                <Badge>Included</Badge>
                            )
                        ) : (
                            <Input
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
                <CardDescription>{product.description}</CardDescription>
            </CardHeader>
            <CardFooter>
                <div className="flex w-full items-end justify-between gap-3 ">
                    <div>
                        <p className="pb-1 text-xs">Total</p>
                        <Badge className="rounded bg-emerald-400 py-2 hover:bg-emerald-400">
                            {product.max_quantity != null &&
                            product.max_quantity <= 1 &&
                            packageProductBaseQuantity > 0
                                ? `Included In ${packageName}`
                                : packageProductBaseQuantity > 0 &&
                                  (selected?.quantity ?? 0) <= 0
                                ? "0 kr"
                                : `${formatCurrency(
                                      productWithAdjustedPrice?.adjustedPrice ??
                                          NaN
                                  )} kr`}
                        </Badge>
                    </div>
                    <div className="flex gap-3">
                        {selected != null && selected.quantity > 1 && (
                            <div>
                                <p className="pb-1 text-xs">Unit price</p>
                                <Badge
                                    className="rounded p-2"
                                    variant={"outline"}
                                >
                                    {formatCurrency(productAdjustedUnitPrice)}{" "}
                                    kr
                                </Badge>
                            </div>
                        )}
                        {(product.max_quantity == null ||
                            product.max_quantity > 1) &&
                            packageProductBaseQuantity > 0 && (
                                <Tooltip>
                                    <TooltipTrigger>
                                        <div className="text-start">
                                            <p className="pb-1 text-xs">
                                                Included
                                            </p>
                                            <Badge
                                                className="rounded py-2 "
                                                variant={"outline"}
                                            >
                                                {packageProductBaseQuantity}{" "}
                                                included in {packageName}
                                            </Badge>
                                        </div>
                                    </TooltipTrigger>
                                    <TooltipContent className="max-w-[400px] p-2">
                                        <p>
                                            You have selected the{" "}
                                            <span className="rounded bg-stone-200 p-1 text-xs">
                                                {packageName}
                                            </span>{" "}
                                            package, which gives you{" "}
                                            {packageProductBaseQuantity}{" "}
                                            {product.name.toLowerCase()} in
                                            addition to whatever you buy here
                                        </p>
                                    </TooltipContent>
                                </Tooltip>
                            )}
                    </div>
                </div>
            </CardFooter>
        </Card>
    )
}
