import { createSelector as cs } from "@reduxjs/toolkit"
import { RootState } from "../store"
import {
    PACKAGE_KEY,
    EVENTS_REGISTRATION_SECTION_KEY,
    EXTRAS_REGISTRATION_SECTION_KEY
} from "../../shared/vars"

export const selectProducts = (state: RootState) => state.products
export const selectProduct = cs(
    selectProducts,
    (_: RootState, productId: number) => productId,
    (products, productId) =>
        products.records.find(current => current.id === productId)
)
export const selectProductPackages = cs(selectProducts, products =>
    products.records.filter(current => current.category?.name === "Package")
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
                current.category?.name !== PACKAGE_KEY
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
