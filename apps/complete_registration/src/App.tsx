import { FormScreen } from "./screens/form/screen"
import { useSelector } from "react-redux"
import { selectActiveForm } from "./store/form/form_selectors"
import { useEffect, useRef } from "react"
import { reverseMap } from "./utils/mapper"
import { useDispatch } from "react-redux"
import { setErrors, setField } from "./store/form/form_slice"
import {
    PACKAGE_KEY,
    ProductMeta,
    loadProducts,
    pickProduct
} from "./store/products/products_slice"
import { DashboardScreen } from "./screens/dashboard/screen"
import {
    RegistrationStatus,
    setCompanyName,
    setCompanyRegistrationStatus,
    setUser
} from "./store/company/company_slice"

export const HOST = ""

export function App() {
    const initialized = useRef(false)
    const dispatch = useDispatch()
    const form = useSelector(selectActiveForm)

    useEffect(() => {
        if (initialized.current) return
        initialized.current = true

        fetch(`${HOST}/api/accounting/products`).then(async raw => {
            const data = await raw.json()
            console.log("PRODUCTS", data)
            dispatch(loadProducts(data))
        })
        fetch(`${HOST}/api/registration/`, {
            headers: new Headers({
                "ngrok-skip-browser-warning": "69420"
            })
        }).then(async raw => {
            const data = await raw.json()
            console.log(JSON.stringify(data))

            if (data.error != null) {
                console.log("Setting", data.error)
                dispatch(setErrors(data.error))
            }

            const awaitingMappings = reverseMap(data)

            // Set status for company
            dispatch(
                setCompanyRegistrationStatus(data.type as RegistrationStatus)
            )
            dispatch(setCompanyName(data.company.name))
            dispatch(setUser(data.contact))

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
