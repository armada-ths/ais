import { createSlice, PayloadAction } from "@reduxjs/toolkit"

export interface Category {
    name: "Package" | "Additional booth area"
    allow_multiple_purchases: boolean
}

export interface RegistrationSection {
    id: string
    name: string
    description: string
    hide_from_registration: boolean
}

export interface Product {
    id: number
    name: string
    max_quantity: number
    unit_price: number
    description: string
    category: Category | null
    no_customer_removal: boolean
    registration_section: RegistrationSection | null
    child_products: Omit<Product, "child_products">[]
}
export interface ProductMeta {
    id: number
    unit_price: number | null
    comment: string
    product: Product
    quantity: number
}

export interface SelectedProduct {
    id: number
    quantity: number
    isPackage: boolean
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

export const PACKAGE_KEY = "Package"
export const EVENTS_REGISTRATION_SECTION_KEY = "Events"
export const EXTRAS_REGISTRATION_SECTION_KEY = "Extras"

export const productSlice = createSlice({
    name: "products",
    initialState,
    reducers: {
        loadProducts: (state, action: PayloadAction<Product[]>) => {
            state.records = action.payload
        },
        pickProduct: (state, action: PayloadAction<SelectedProduct>) => {
            // Remove previous occurances of the product
            state.selected = state.selected.filter(
                current => current.id !== action.payload.id
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
export const { loadProducts, pickProduct, unpickProduct } = productSlice.actions

export default productSlice.reducer
