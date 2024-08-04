import {
    Tooltip,
    TooltipContent,
    TooltipTrigger
} from "@/components/ui/tooltip"
import { getProductWithAdjustedPrice } from "@/forms/fr_accounting/accounting_utilities"
import { Product } from "@/shared/hooks/api/useDashboard"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { formatCurrency } from "@/utils/format_currency"
import { Card } from "./PageCard"

export default function ProductCard({ product }: { product: Product }) {
    const { data: orders } = useOrders()

    const productWithAdjustedPrice = getProductWithAdjustedPrice(
        product.id,
        orders,
        [product]
    )
    const order = orders.find(order => order.product.id === product.id)

    const unitPrice = productWithAdjustedPrice?.unit_price
    return (
        <Tooltip>
            <TooltipTrigger>
                <Card key={product.id} className="text-left">
                    <p className="">{product.short_name || product.name}</p>
                    {order != null && order?.quantity > 1 && (
                        <p className="mt-2 text-slate-400">
                            {formatCurrency(unitPrice)} kr x{" "}
                            {order?.quantity ?? 1}
                        </p>
                    )}
                    <p className="text-slate-400">
                        Total:{" "}
                        {formatCurrency(
                            productWithAdjustedPrice?.adjustedPrice
                        )}{" "}
                        kr
                    </p>
                </Card>
            </TooltipTrigger>
            <TooltipContent>
                <div className="max-w-[350px]">{product.description}</div>
            </TooltipContent>
        </Tooltip>
    )
}
