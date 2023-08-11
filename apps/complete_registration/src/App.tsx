import { FormScreen } from "./screens/form/screen"
import { useSelector } from "react-redux"
import { selectActiveForm } from "./store/form/form_selectors"
import { useEffect, useRef } from "react"
import { reverseMap } from "./utils/mapper"
import { useDispatch } from "react-redux"
import { setField } from "./store/form/form_slice"
import {
    PACKAGE_KEY,
    ProductMeta,
    loadProducts,
    pickProduct
} from "./store/products/products_slice"
import { DashboardScreen } from "./screens/dashboard/screen"

export const HOST = "http://192.168.157.172:3000"

export function App() {
    const initialized = useRef(false)
    const dispatch = useDispatch()
    const form = useSelector(selectActiveForm)

    useEffect(() => {
        if (initialized.current) return
        initialized.current = true

        fetch(`${HOST}/api/accounting/products`).then(async raw => {
            const data = await raw.json()
            dispatch(loadProducts(data))
        })
        fetch(`${HOST}/api/registration/`, {
            headers: new Headers({
                "ngrok-skip-browser-warning": "69420"
            })
        }).then(async raw => {
            const data = await raw.json()
            const awaitingMappings = reverseMap(data)

            for (const current of awaitingMappings) {
                dispatch(
                    setField({
                        mapping: current.mapping,
                        value: current.value
                    })
                )
            }

            // Apply orders
            const orders = data.orders as ProductMeta[]
            for (const productMeta of orders) {
                dispatch(
                    pickProduct({
                        id: productMeta.product.id,
                        quantity: productMeta.quantity,
                        isPackage:
                            productMeta.product.category?.name === PACKAGE_KEY
                    })
                )
            }
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <div className="bg-slate-50">
            {form ? <FormScreen form={form} /> : <DashboardScreen />}
        </div>
    )
}