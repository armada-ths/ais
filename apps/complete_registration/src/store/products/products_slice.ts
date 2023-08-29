import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { PACKAGE_KEY } from "../../shared/vars"

export interface Category {
    id: number
    name: "Package" | "Additional booth area" | "Non Visible Package"
    description: string
    allow_multiple_purchases: boolean
}

export interface RegistrationSection {
    id: string
    name: string
    description: string
    hide_from_registration: boolean
}

export interface ChildProduct {
    quantity: number
    child_product: Omit<Product, "child_products">
}

export interface Product {
    id: number
    name: string
    short_name: string
    max_quantity: number
    unit_price: number
    description: string
    category: Category | null
    display_in_product_list: boolean
    registration_section: RegistrationSection | null
    child_products: ChildProduct[]
}
export interface ProductAdjustedPrice extends Product {
    price: number
}

export interface SelectedProduct {
    id: number
    quantity: number
    isPackage: boolean
    adjustedPrice?: number
    comment?: string
}

export interface ProductState {
    records: Product[]
    selected: SelectedProduct[]
}

const initialState: ProductState = {
    records: [],
    selected: []
}

export function generateProductApiSetArray(selected: SelectedProduct[]) {
    return selected.map(product => ({
        product: {
            id: product.id
        },
        quantity: product.quantity // Hard coded for now, sorry :(
    }))
}

export const productSlice = createSlice({
    name: "products",
    initialState,
    reducers: {
        loadProducts: (state, action: PayloadAction<Product[]>) => {
            action.payload.forEach(console.log)
            state.records = action.payload.filter(
                product => product.display_in_product_list
            )
        },
        loadProductMeta: (
            state,
            action: PayloadAction<Omit<SelectedProduct, "isPackage">[]>
        ) => {
            action.payload.map(adjustedPrice => {
                const selectedProduct = state.selected.find(
                    selected => selected.id === adjustedPrice.id
                )
                if (selectedProduct) {
                    selectedProduct.quantity = adjustedPrice.quantity
                    selectedProduct.comment = adjustedPrice.comment
                    selectedProduct.adjustedPrice = adjustedPrice.adjustedPrice
                    return
                }
                const product = state.records.find(
                    product => product.id === adjustedPrice.id
                )
                if (product != null) {
                    state.selected.push({
                        id: product.id,
                        isPackage: product.category?.name === PACKAGE_KEY,
                        quantity: adjustedPrice.quantity,
                        comment: adjustedPrice.comment
                    })
                    return
                }
                console.warn("Product not found", action.payload)
            })
        },
        pickProduct: (state, action: PayloadAction<SelectedProduct>) => {
            // If selected package, clear all products
            if (action.payload.isPackage) {
                state.selected = [action.payload]
                return
            }
            // Remove previous occurances of the product
            state.selected = state.selected.filter(
                current =>
                    // Always delete duplicates
                    current.id !== action.payload.id &&
                    // If the product is a package, delete other packages if they exist
                    (action.payload.isPackage && current.isPackage) === false
            )
            state.selected.push(action.payload)
        },
        unpickProduct: (
            state,
            action: PayloadAction<{
                id: number
            }>
        ) => {
            state.selected = state.selected.filter(
                current => current.id !== action.payload.id
            )
        }
    }
})

// Action creators are generated for each case reducer function
export const { loadProducts, loadProductMeta, pickProduct, unpickProduct } =
    productSlice.actions

export default productSlice.reducer
