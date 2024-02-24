import {
    RegistrationStatus,
    setCompanyName,
    setCompanyRegistrationStatus,
    setContract,
    setUser
} from "@/store/company/company_slice"
import { setErrors, setField } from "@/store/form/form_slice"
import {
    SelectedProduct,
    loadProductMeta,
    loadProducts,
    pickProduct
} from "@/store/products/products_slice"
import { reverseMap } from "@/utils/mapper"
import { useEffect, useRef, useState } from "react"
import { useDispatch } from "react-redux"
import { HOST, PACKAGE_KEY } from "./vars"

export default function useLoadData() {
    const initialized = useRef(false)
    const [loading, setLoading] = useState(true)
    const dispatch = useDispatch()

    useEffect(() => {
        if (initialized.current) return
        initialized.current = true

        async function load() {
            /*             const data = await fetch(`${HOST}/api/accounting/products`).then(
                raw => raw.json()
            )
            console.log("PRODUCTS", JSON.stringify(data)) */

            fetch(`${HOST}/api/dashboard/`, {}).then(async raw => {
                const data = await raw.json()

                // Load products
                const products = data.products
                dispatch(loadProducts(products))

                if (data.error != null) {
                    dispatch(setErrors(data.error))
                }

                const awaitingMappings = reverseMap(data)
                // Set status for company
                dispatch(
                    setCompanyRegistrationStatus(
                        data.type as RegistrationStatus
                    )
                )
                if (data.company?.name) {
                    dispatch(setCompanyName(data.company.name))

                    //Get Lunch Tickets

                    fetch(
                        `${HOST}/api/fair/lunchtickets/companysearch?company=${data.company.name}`
                    ).then(async raw => {
                        const data = await raw.json()
                        //data.result[0].id
                        const maps = reverseMap(data)
                        for (const current of maps) {
                            dispatch(
                                setField({
                                    mapping: current.mapping,
                                    value: current.value
                                })
                            )
                        }
                    })
                }

                if (data.contact) dispatch(setUser(data.contact))
                if (data.contract) dispatch(setContract(data.contract))

                for (const current of awaitingMappings) {
                    dispatch(
                        setField({
                            mapping: current.mapping,
                            value: current.value
                        })
                    )
                }

                // Apply orders
                const orders = data.orders
                for (const productMeta of orders ?? []) {
                    dispatch(
                        pickProduct({
                            id: productMeta.product.id,
                            quantity: productMeta.quantity,
                            isPackage:
                                productMeta.product.category?.name ===
                                PACKAGE_KEY
                        })
                    )
                }

                const productMetas = data.orders
                const customPrices = [] as Omit<SelectedProduct, "isPackage">[]

                for (const productMeta of productMetas ?? []) {
                    // eslint-disable-next-line @typescript-eslint/no-unused-vars
                    customPrices.push({
                        id: productMeta.product.id,
                        comment: productMeta.comment,
                        quantity: productMeta.quantity,
                        adjustedPrice: productMeta.unit_price
                    })
                }
                dispatch(loadProductMeta(customPrices))
                setLoading(false)
            })
        }

        load()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return {
        initialized: !loading
    }
}
