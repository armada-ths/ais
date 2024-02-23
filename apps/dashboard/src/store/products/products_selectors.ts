import { createSelector as cs } from "@reduxjs/toolkit"
import {
    EVENTS_REGISTRATION_SECTION_KEY,
    EXTRAS_REGISTRATION_SECTION_KEY,
    PACKAGE_KEY,
    PACKAGE_NOT_VISIBLE_KEY
} from "../../shared/vars"
import { RootState } from "../store"

export function selectProducts(state: RootState) {
    return state.products
}
export const selectProduct = cs(
    selectProducts,
    (_: RootState, productId: number) => productId,
    (products, productId) =>
        products.records.find(current => current.id === productId)
)
export const selectProductPackages = cs(selectProducts, products =>
    products.records.filter(
        current =>
            current.category?.name.toLowerCase() === "package" ||
            current.category?.name.toLowerCase() === "non visible package"
    )
)
export const selectVisibleProductPackages = cs(
    selectProductPackages,
    packages =>
        packages.filter(
            current => current.category?.name.toLowerCase() === "package"
        )
)
export const selectSelectedProducts = cs(
    selectProducts,
    products => products.selected
)
export const selectProductsSelectedWithoutPackages = cs(
    [selectSelectedProducts, selectProducts],
    (selected, products) =>
        products.records.filter(
            current =>
                selected.map(current => current.id).includes(current.id) &&
                current.category?.name.toLowerCase() !==
                    PACKAGE_KEY.toLowerCase() &&
                current.category?.name.toLowerCase() !==
                    PACKAGE_NOT_VISIBLE_KEY.toLowerCase()
        )
)
export const selectProductsSelectedWithoutPackagesWithAdjustedPrice = cs(
    [(state: RootState) => state, selectProductsSelectedWithoutPackages],
    (state, selected) =>
        selected.map(current => ({
            ...current,
            price: selectAdjustedProductPrice(state, current.id)
        }))
)
export const selectProductPackage = cs(
    [selectProductPackages, selectSelectedProducts],
    (packages, selected) =>
        packages.find(current =>
            selected.map(current => current.id).includes(current.id)
        )
)

export const selectProductEvents = cs(selectProducts, products =>
    products.records.filter(
        current =>
            current.registration_section?.name ===
            EVENTS_REGISTRATION_SECTION_KEY
    )
)

export const selectProductExtras = cs(selectProducts, products =>
    products.records.filter(
        current =>
            current.registration_section?.name ===
            EXTRAS_REGISTRATION_SECTION_KEY
    )
)

export const selectSelectedProduct = cs(
    [
        selectSelectedProducts,
        (_state: RootState, productId: number) => productId
    ],
    (selectedProducts, productId) =>
        selectedProducts.find(current => current.id === productId)
)
export const selectAdjustedProductPrice = cs(
    [selectProduct, selectSelectedProduct],
    (product, productMeta) => {
        return (
            (productMeta?.quantity ?? 1) *
            (productMeta?.adjustedPrice ?? product?.unit_price ?? 0)
        )
    }
)
// Same as selectAdjustedProductPrice but without quantity
export const selectUnitAdjustedProductPrice = cs(
    [selectProduct, selectSelectedProduct],
    (product, productMeta) =>
        productMeta?.adjustedPrice ?? product?.unit_price ?? 0
)

export const selectPackageBaseProductQuantity = cs(
    [(_: RootState, productId: number) => productId, selectProductPackage],
    (productId, productPackage) => {
        if (!productPackage) return 0
        return (
            productPackage.child_products.find(
                current => current.child_product.id === productId
            )?.quantity ?? 0
        )
    }
)
