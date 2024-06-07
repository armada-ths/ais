import { Product } from "@/store/products/products_slice"
import { formatCurrency } from "@/utils/format_currency"

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
