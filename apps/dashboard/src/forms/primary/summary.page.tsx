import { useNavigate } from "@tanstack/react-router"
import { Button } from "primereact/button"
import { Checkbox } from "primereact/checkbox"
import { ConfirmPopup, confirmPopup } from "primereact/confirmpopup"
import { Toast } from "primereact/toast"
import { MouseEvent, useRef, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { Card } from "../../screens/form/sidebar/PageCard"
import { HOST } from "../../shared/vars"
import { selectCompany } from "../../store/company/company_selectors"
import { setCompanyRegistrationStatus } from "../../store/company/company_slice"
import {
    selectActiveForm,
    selectUnfilledFields
} from "../../store/form/form_selectors"
import { setActiveForm } from "../../store/form/form_slice"
import {
    selectProductPackage,
    selectProductsSelectedWithoutPackagesWithAdjustedPrice
} from "../../store/products/products_selectors"
import { RootState } from "../../store/store"
import { formatCurrency } from "../../utils/format_currency"

export function SummaryFormPage() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const toastRef = useRef<Toast>(null)
    const [confirmTerms, setConfirmTerms] = useState(false)
    const [confirmBinding, setConfirmBinding] = useState(false)
    const [confirmEligibility, setConfirmEligibility] = useState(false)
    const productPackage = useSelector(selectProductPackage)

    const company = useSelector(selectCompany)
    const selectedProducts = useSelector(
        selectProductsSelectedWithoutPackagesWithAdjustedPrice
    )

    const activeForm = useSelector(selectActiveForm)
    const unfilledFields = useSelector((state: RootState) =>
        selectUnfilledFields(state, activeForm?.key ?? "primary")
    )

    const readyToSign =
        confirmTerms &&
        confirmBinding &&
        confirmEligibility &&
        unfilledFields.length === 0 &&
        productPackage != null

    async function submitRegistration() {
        const response = await fetch(`${HOST}/api/dashboard/submit`, {
            method: "POST"
        })
        if (response.status < 200 || response.status >= 300) {
            toastRef.current?.show({
                severity: "error",
                summary: "Error",
                detail: "We encountered an error while submitting, if the problem persists please contact us."
            })
            return
        }

        dispatch(setCompanyRegistrationStatus("complete_registration_signed"))
        dispatch(setActiveForm(null))
        navigate({
            to: "/"
        })
    }

    const confirm = (event: MouseEvent<HTMLButtonElement>) => {
        confirmPopup({
            target: event.currentTarget,
            message: (
                <div className="flex flex-col">
                    <p>
                        Have you filled in everything you want? Once your Final
                        Registration has been made, you can only make changes by
                        contacting us.
                    </p>
                </div>
            ),
            icon: "pi pi-info-circle",
            accept: submitRegistration,
            reject: () => {}
        })
    }

    const totalPrice =
        selectedProducts.reduce((acc, current) => acc + current.price, 0) +
        (productPackage?.unit_price ?? 0)

    const grossPrice = formatCurrency(totalPrice * 1.25)

    return (
        <div className="flex flex-col items-center">
            <Toast ref={toastRef} />
            {(unfilledFields.length > 0 || productPackage == null) && (
                <h2 className="mb-2 text-lg text-red-400">
                    Missing information
                </h2>
            )}
            <div className="mb-5 flex gap-5">
                {productPackage == null && (
                    <p className="mb-1 text-sm">No package selected</p>
                )}
                {unfilledFields.map(current => (
                    <Card key={current.page.id}>
                        <h3 className="mb-2">{current.page.title}</h3>
                        {current.fields.map(field => (
                            <p key={field.mapping} className="mb-1 text-sm">
                                {field.mapping}
                            </p>
                        ))}
                    </Card>
                ))}
            </div>
            <div className="flex flex-col justify-center gap-4">
                <div className="flex items-center gap-x-5">
                    <Checkbox
                        checked={confirmTerms}
                        className=""
                        onChange={value =>
                            setConfirmTerms(value.checked ?? false)
                        }
                    />
                    <p>
                        I have read and understand the{" "}
                        <a
                            className="font-medium text-blue-600 hover:underline dark:text-blue-500"
                            href={company.contract?.contract ?? ""}
                            target="_blank"
                        >
                            Armada Terms and Conditions.
                        </a>
                    </p>
                </div>

                <div className="flex items-center gap-x-5">
                    <Checkbox
                        checked={confirmBinding}
                        className=""
                        onChange={value =>
                            setConfirmBinding(value.checked ?? false)
                        }
                    />
                    <p>
                        I understand that the Final Registration is binding and{" "}
                        <i>{company.companyName}</i> will be invoiced{" "}
                        <b>{grossPrice} kr</b> inc. VAT, by THS Armada, through
                        Tekniska Högskolans Studentkår, org. nr. 802005-9153
                    </p>
                </div>

                <div className="flex items-center gap-x-5">
                    <Checkbox
                        checked={confirmEligibility}
                        className=""
                        onChange={value =>
                            setConfirmEligibility(value.checked ?? false)
                        }
                    />
                    <p>
                        I have the authority to enter into this agreement on
                        behalf of <i>{company.companyName}</i>
                    </p>
                </div>
            </div>
            <div className="mt-16 flex justify-center">
                <ConfirmPopup />
                <div className="card justify-content-center flex flex-wrap gap-2 whitespace-nowrap">
                    <Button
                        onClick={confirm}
                        disabled={!readyToSign}
                        icon="pi pi-check"
                        label="Confirm Final Registration"
                    />
                </div>
            </div>
            <div
                className="my-10 text-sm text-slate-400"
                style={{ maxWidth: "50rem" }}
            >
                THS Armada will process any personal information you leave in
                this registration on the basis of legitimate interests. Your
                information will not be shared outside of THS (org. nr.
                802005-9153) and be used to provide you the services you order
                and to offer you similar services in the future. You are,
                according to GDPR , entitled to receive information regarding
                what personal data we process and how we process these. You also
                have the right to request a correction as to what personal data
                we are processing about you. To exercise these rights, contact
                a@armada.nu.
            </div>
        </div>
    )
}
