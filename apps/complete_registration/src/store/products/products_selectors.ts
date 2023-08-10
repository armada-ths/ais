import { createSelector as cs } from "@reduxjs/toolkit"
import { RootState } from "../store"
import { EVENTS_REGISTRATION_SECTION_KEY } from "./products_slice"

export const selectProducts = (state: RootState) => state.products
export const selectProductPackages = cs(selectProducts, products =>
    products.records.filter(current => current.category?.name === "Package")
)
export const selectSelectedProducts = cs(
    selectProducts,
    products => products.selected
)

export const selectProductEvents = cs(selectProducts, products =>
    products.records.filter(
        current =>
            current.registration_section?.name ===
            EVENTS_REGISTRATION_SECTION_KEY
    )
)

export const selectSelectedProduct = cs(
    [
        selectSelectedProducts,
        (state: RootState, productId: number) => productId
    ],
    (selectedProducts, productId) =>
        selectedProducts.find(current => current.id === productId)
)
