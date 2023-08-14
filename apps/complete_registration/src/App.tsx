import { FormScreen } from "./screens/form/screen"
import { useSelector } from "react-redux"
import { selectActiveForm } from "./store/form/form_selectors"
import { useEffect, useRef } from "react"
import { reverseMap } from "./utils/mapper"
import { useDispatch } from "react-redux"
import { setErrors, setField } from "./store/form/form_slice"
import {
    SelectedProduct,
    loadProductMeta,
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
import { HOST, PACKAGE_KEY } from "./shared/vars"

export function App() {
    const initialized = useRef(false)
    const dispatch = useDispatch()
    const form = useSelector(selectActiveForm)

    useEffect(() => {
        if (initialized.current) return
        initialized.current = true

        fetch(`${HOST}/api/accounting/products`).then(async raw => {
            const data = await raw.json()
            console.log("PRODUCS", JSON.stringify(data))
            dispatch(loadProducts(data))
        })
        fetch(`${HOST}/api/registration/`, {}).then(async raw => {
            const data = await raw.json()
            console.log("DATA", JSON.stringify(data))

            if (data.error != null) {
                dispatch(setErrors(data.error))
            }

            const awaitingMappings = reverseMap(data)

            // Set status for company
            dispatch(
                setCompanyRegistrationStatus(data.type as RegistrationStatus)
            )
            if (data.company?.name) dispatch(setCompanyName(data.company.name))
            if (data.contact) dispatch(setUser(data.contact))

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
                            productMeta.product.category?.name === PACKAGE_KEY
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
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <div className="bg-slate-50">
            {form ? <FormScreen form={form} /> : <DashboardScreen />}
        </div>
    )
}
