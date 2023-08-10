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
    category: Category
    no_customer_removal: boolean
    child_products: Omit<Product, "child_products">[]
}

export interface ProductState {
    records: Product[]
    selected: Product[]
}

const initialState: ProductState = {
    records: [],
    selected: []
}

export function generateProductApiSetArray(selected: Product[]) {
    return selected.map(product => ({
        product: {
            id: product.id
        },
        quantity: 1 // Hard coded for now, sorry :(
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
        selectPackage: (state, action: PayloadAction<Product>) => {
            const oldProducts = state.selected
            state.selected = oldProducts.filter(
                product => product.category.name !== PACKAGE_KEY
            )
            state.selected.push(action.payload)
        }
    }
})

// Action creators are generated for each case reducer function
export const { loadProducts, selectPackage } = productSlice.actions

export default productSlice.reducer
