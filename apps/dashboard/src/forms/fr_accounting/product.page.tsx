import { belongsToSection } from "@/forms/fr_accounting/accounting_utilities"
import { DiscountCard } from "@/forms/fr_accounting/components/DiscountCard"
import { ProductOrderingCard } from "@/forms/fr_accounting/components/ProductOrderingCard"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { RegistrationSection } from "@/shared/vars"
import React, { useMemo } from "react"
import { Category, Product } from "../../store/products/products_slice"
import { FormWrapper } from "../FormWrapper"

export function ProductFormPage({ section }: { section: RegistrationSection }) {
    const { data: allProducts } = useProducts()
    const products = allProducts.filter(product =>
        belongsToSection(product, section)
    )

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
                                            <ProductOrderingCard
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
