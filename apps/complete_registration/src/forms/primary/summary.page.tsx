import { Button } from "primereact/button"
import { Checkbox } from "primereact/checkbox"
import { useState, MouseEvent, useRef } from "react"
import { useDispatch, useSelector } from "react-redux"
import {
    selectActiveForm,
    selectUnfilledFields
} from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { Card } from "../../screens/form/sidebar/PageCard"
import { ConfirmPopup, confirmPopup } from "primereact/confirmpopup"
import { setCompanyRegistrationStatus } from "../../store/company/company_slice"
import { setActiveForm } from "../../store/form/form_slice"
import { Toast } from "primereact/toast"
import { HOST } from "../../shared/vars"

export function SummaryFormPage() {
    const dispatch = useDispatch()
    const toastRef = useRef<Toast>(null)
    const [confirmEligibility, setConfirmEligibility] = useState(false)
    const [confirmDataProcessing, setConfirmDataProcessing] = useState(false)

    const activeForm = useSelector(selectActiveForm)
    const unfilledFields = useSelector((state: RootState) =>
        selectUnfilledFields(state, activeForm?.key ?? "primary")
    )

    const readyToSign =
        confirmEligibility &&
        confirmDataProcessing &&
        unfilledFields.length === 0

    async function submitRegistration() {
        const response = await fetch(`${HOST}/api/registration/submit`, {
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
    }

    const confirm = (event: MouseEvent<HTMLButtonElement>) => {
        confirmPopup({
            target: event.currentTarget,
            message: (
                <div className="flex flex-col">
                    <p>Lock your product selection</p>
                </div>
            ),
            icon: "pi pi-info-circle",
            accept: submitRegistration,
            reject: () => {}
        })
    }

    return (
        <div className="flex flex-col items-center">
            <Toast ref={toastRef} />
            {unfilledFields.length > 0 && (
                <h2 className="mb-2 text-lg text-red-400">
                    Missing information
                </h2>
            )}
            <div className="mb-5 flex gap-5">
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
            <div className="mb-5 flex flex-col justify-center">
                <div className="flex items-center gap-x-5">
                    <Checkbox
                        checked={confirmEligibility}
                        className=""
                        onChange={value =>
                            setConfirmEligibility(value.checked ?? false)
                        }
                    />
                    <p>I'm eligible to sign this</p>
                </div>

                <div className="mt-5 flex items-center gap-x-5">
                    <Checkbox
                        checked={confirmDataProcessing}
                        className=""
                        onChange={value =>
                            setConfirmDataProcessing(value.checked ?? false)
                        }
                    />
                    <p className="text-xs text-slate-500">
                        THS Armada would like to process personal data about you
                        and your organization to be able to contact you in
                        conjunction with complete registration and send you
                        information regarding the fair of 2023. The data we
                        intend to collect and the process is forename, surname,
                        the title of your organization, phone number, and email
                        address. You decide for yourself if you want to leave
                        any additional information to us. The data will only be
                        processed by the project group in THS Armada and by THS
                        Management. The data will be saved in the Armada
                        Internal Systems, AIS. You are, according to GDPR
                        (General Data Protection Regulation), entitled to
                        receive information regarding what personal data we
                        process and how we process these. You also have the
                        right to request a correction as to what personal data
                        we are processing about you. I consent for THS Armada to
                        process my personal data in accordance with the above.*
                    </p>
                </div>
            </div>
            <div className="flex w-60 justify-center">
                <ConfirmPopup />
                <div className="card justify-content-center flex flex-wrap gap-2">
                    <Button
                        onClick={confirm}
                        disabled={!readyToSign}
                        icon="pi pi-check"
                        label="Place Order"
                    />
                </div>
            </div>
        </div>
    )
}
