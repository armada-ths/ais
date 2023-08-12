import { useSelector } from "react-redux"
import { FormWrapper } from "../FormWrapper"
import { selectField } from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { CompleteButton } from "../../shared/CompleteButton"

export function TransportSummaryFormPage() {
    const transportFrom = useSelector((state: RootState) =>
        selectField(state, "exhibitor.transport_from")
    )
    const transportTo = useSelector((state: RootState) =>
        selectField(state, "exhibitor.transport_to")
    )
    return (
        <FormWrapper>
            <div className="flex flex-col gap-5">
                <div className="flex items-center justify-between">
                    <p className="">Transport from fair: </p>
                    <span className="rounded bg-slate-400 p-2 px-3 text-white">
                        {transportFrom?.value?.toString() ?? "unknown"}
                    </span>
                </div>
                <div className="flex items-center justify-between">
                    <p className="">Transport to fair: </p>
                    <span className="rounded bg-slate-400 p-2 px-3 text-white">
                        {transportTo?.value?.toString() ?? "unknown"}
                    </span>
                </div>
            </div>
            <div className="mt-10 flex flex-1 justify-center">
                <CompleteButton />
            </div>
        </FormWrapper>
    )
}
