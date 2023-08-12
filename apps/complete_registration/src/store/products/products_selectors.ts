import { createSelector as cs } from "@reduxjs/toolkit"
import { RootState } from "../store"
import {
    EVENTS_REGISTRATION_SECTION_KEY,
    EXTRAS_REGISTRATION_SECTION_KEY,
    PACKAGE_KEY
} from "./products_slice"

export const selectProducts = (state: RootState) => state.products
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
