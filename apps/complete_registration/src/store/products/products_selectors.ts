import { createSelector as cs } from "@reduxjs/toolkit"
import { RootState } from "../store"

export const selectProducts = (state: RootState) => state.products
export const selectProductPackages = cs(selectProducts, products =>
    products.records.filter(current => current.category.name === "Package")
)
export const selectSelectedProducts = cs(
    selectProducts,
    products => products.selected
)
