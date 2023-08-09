import { FormScreen } from "./screens/form/screen"
import { useSelector } from "react-redux"
import { selectForm } from "./store/form/form_selectors"
import { useEffect } from "react"
import { reverseMap } from "./utils/mapper"
import { useDispatch } from "react-redux"
import { setField } from "./store/form/form_slice"

interface RegistrationForm {
    invoiceDetails: {
        orgName: string
        orgCorpId: string
        legalOrgName: string
        contactEmails: string[]
        invoiceAddresses: string[]
        invoiceZipCode: string
        invoiceCity: string
        invoiceCountry: string
        invoiceReference: string
        invoiceEmail: string
    }
    cart: {
        package: "bronze" | "silver" | "gold"
        products: Array<{
            productId: string
            name: string
        }>
    }
}

export function App() {
    const dispatch = useDispatch()
    const form = useSelector(selectForm)

    useEffect(() => {
        fetch("http://192.168.157.172:3000/api/registration/", {
            headers: new Headers({
                "ngrok-skip-browser-warning": "69420"
            })
        }).then(async raw => {
            const data = await raw.json()
            const awaitingMappings = reverseMap(data, form)
            for (const current of awaitingMappings) {
                dispatch(
                    setField({
                        mapping: current.mapping,
                        value: current.value
                    })
                )
            }
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <div>
            <FormScreen form={form} />
        </div>
    )
}
