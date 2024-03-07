import {
    selectAdjustedProductPrice,
    selectSelectedProduct,
    selectUnitAdjustedProductPrice
} from "@/store/products/products_selectors"
import { ProductAdjustedPrice } from "@/store/products/products_slice"
import { RootState } from "@/store/store"
import { formatCurrency } from "@/utils/format_currency"
import { useSelector } from "react-redux"
import { Card } from "./PageCard"

export default function ProductCard({
    product
}: {
    product: ProductAdjustedPrice
}) {
    const totalPrice = useSelector((state: RootState) =>
        selectAdjustedProductPrice(state, product.id)
    )
    const productMeta = useSelector((state: RootState) =>
        selectSelectedProduct(state, product.id)
    )
    const unitPrice = useSelector((state: RootState) =>
        selectUnitAdjustedProductPrice(state, product.id)
    )
    return (
        <Card key={product.id} className="">
            <p className="">{product.short_name || product.name}</p>
            {productMeta != null && productMeta?.quantity > 1 && (
                <p className="mt-2 text-slate-400">
                    {unitPrice} kr x {productMeta?.quantity ?? 1}
                </p>
            )}
            <p className="text-slate-400">
                Total: {formatCurrency(totalPrice)} kr
            </p>
        </Card>
    )
}
