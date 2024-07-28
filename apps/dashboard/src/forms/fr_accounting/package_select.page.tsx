import { Badge } from "@/components/ui/badge"
import { getProductWithAdjustedPrice } from "@/forms/fr_accounting/accounting_utilities"
import { useAccountingMutation } from "@/forms/fr_accounting/useAccounting"
import { Product } from "@/shared/hooks/api/useDashboard"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { PACKAGE_SECTION_KEY } from "@/shared/vars"
import { cn } from "@/utils/cx"
import { formatCurrency } from "@/utils/format_currency"
import { FormWrapper } from "../FormWrapper"

export function PackageSelectFormPage() {
    const { data: products, updateCache } = useProducts()
    const { data: orders } = useOrders()
    const packages =
        products?.filter(
            x =>
                x.registration_section?.name.toLowerCase() ===
                PACKAGE_SECTION_KEY.toLowerCase()
        ) ?? []

    const { mutateAsync, isPending } = useAccountingMutation({
        onSuccess: updateCache
    })

    async function onClickPackage(product: Product) {
        await mutateAsync([
            {
                product: {
                    id: product.id
                },
                quantity: 1
            }
        ])
    }

    return (
        <FormWrapper>
            <div className="flex flex-wrap justify-center gap-5">
                {packages.map(product => (
                    <div key={product.id}>
                        <div
                            className={cn(
                                "flex w-72 select-none flex-col rounded-lg border-2 border-slate-500 transition-all duration-200 hover:cursor-pointer active:scale-95",
                                {
                                    "opacity-20": isPending,
                                    "border-melon-700": orders.find(
                                        x => x.product.id === product.id
                                    )
                                }
                            )}
                            onClick={() => onClickPackage(product)}
                        >
                            <div>
                                <h2 className="my-5 text-center text-xl text-slate-500">
                                    {product.short_name || product.name}
                                </h2>
                            </div>
                            <div className="mx-5 h-0.5 bg-slate-500" />
                            <div>
                                {product.child_products.map(
                                    ({ child_product, quantity }) => (
                                        <div
                                            key={child_product.id}
                                            className="m-5 flex items-center gap-5 text-sm"
                                        >
                                            <i className="pi pi-check !font-bold text-emerald-400"></i>
                                            <div className="flex gap-1 text-slate-500">
                                                <p className="">
                                                    {child_product.short_name ||
                                                        child_product.name}
                                                </p>
                                                {quantity > 1 && (
                                                    <p> x {quantity}</p>
                                                )}
                                            </div>
                                        </div>
                                    )
                                )}
                            </div>
                            <div className="flex flex-1 items-end justify-center p-5">
                                <p className="rounded bg-slate-500 p-1 px-3 text-center text-lg font-bold text-slate-50">
                                    {formatCurrency(
                                        getProductWithAdjustedPrice(
                                            product.id,
                                            orders,
                                            products
                                        )?.adjustedPrice ?? NaN
                                    )}{" "}
                                    kr
                                </p>
                            </div>
                        </div>
                        {orders.find(x => x.product.id === product.id) && (
                            <div className="flex items-center justify-center p-2">
                                <Badge className="bg-melon-700 hover:bg-melon-700">
                                    Selected
                                </Badge>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </FormWrapper>
    )
}
