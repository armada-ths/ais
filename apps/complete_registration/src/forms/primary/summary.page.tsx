import { Button } from "primereact/button"
import { Checkbox } from "primereact/checkbox"
import { useState, MouseEvent } from "react"
import { useSelector } from "react-redux"
import {
    selectActiveForm,
    selectUnfilledFields
} from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { Card } from "../../screens/form/sidebar/PageCard"
import { ConfirmPopup, confirmPopup } from "primereact/confirmpopup"
import { HOST } from "../../App"

export function SummaryFormPage() {
    const [confirmEligibility, setConfirmEligibility] = useState(false)

    const activeForm = useSelector(selectActiveForm)
    const selectUnfilled = useSelector((state: RootState) =>
        selectUnfilledFields(state, activeForm?.key ?? "primary")
    )

    const readyToSign = confirmEligibility && selectUnfilled.length === 0

    async function submitRegistration() {
        const response = await fetch(`${HOST}/api/registration/submit`, {
            method: "POST"
        })
        console.log(JSON.stringify(await response.json()))
    }

    const confirm = (event: MouseEvent<HTMLButtonElement>) => {
        confirmPopup({
            target: event.currentTarget,
            message: (
                <div className="flex flex-col">
                    <p>Are you sure you want to continue? </p>
                    <p>This action cannot be undone</p>
                </div>
            ),
            icon: "pi pi-exclamation-triangle",
            accept: submitRegistration,
            reject: () => {}
        })
    }

    return (
        <div className="flex flex-col items-center">
            <h2 className="mb-2 text-lg text-red-400">Missing information</h2>
            <div className="mb-5 flex gap-5">
                {selectUnfilled.map(current => (
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
                    <p>I'm eligible to sign this</p>
                    <Checkbox
                        checked={confirmEligibility}
                        className=""
                        onChange={value =>
                            setConfirmEligibility(value.checked ?? false)
                        }
                    />
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
