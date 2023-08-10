import { createSlice, PayloadAction } from "@reduxjs/toolkit"

export interface Category {
    name: "Package" | "Additional booth area"
    allow_multiple_purchases: boolean
}

export interface Product {
    id: number
    name: string
    max_quantity: number
    unit_price: number
    description: string
    category: Category | null
    no_customer_removal: boolean
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
export const productSlice = createSlice({
    name: "products",
    initialState,
    reducers: {
        loadProducts: (state, action: PayloadAction<Product[]>) => {
            state.records = action.payload
        },
        pickProduct: (state, action: PayloadAction<SelectedProduct>) => {
            if (
                state.selected.find(product => product.id === action.payload.id)
            ) {
                return
            }
            state.selected.push(action.payload)
        }
    }
})

// Action creators are generated for each case reducer function
export const { loadProducts, pickProduct } = productSlice.actions

export default productSlice.reducer
