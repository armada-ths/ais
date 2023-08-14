import { Card } from "./PageCard"
import { ProductAdjustedPrice } from "../../../store/products/products_slice"
import { useSelector } from "react-redux"
import { selectAdjustedProductPrice } from "../../../store/products/products_selectors"
import { RootState } from "../../../store/store"

export default function ProductCard({
    product
}: {
    product: ProductAdjustedPrice
}) {
    const price = useSelector((state: RootState) =>
        selectAdjustedProductPrice(state, product.id)
    )
    return (
        <Card key={product.id} className="">
            <p className="">{product.name}</p>
            <p className="mt-2 text-slate-400">
                {Intl.NumberFormat("sv").format(price)} kr
            </p>
        </Card>
    )
}
