import { useQuery } from "@tanstack/react-query"
import { HOST } from "../vars"

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

export function useProducts() {
    return useQuery({
        queryKey: ["products"],
        queryFn: async () => {
            const response = await fetch(`${HOST}/api/accounting/products`)
            return (await response.json()) as Product[]
        }
    })
}
