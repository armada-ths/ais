import { CompleteButton } from "../../shared/CompleteButton"
import { FormWrapper } from "../FormWrapper"

export function CommingSoon() {
    return (
        <FormWrapper className="flex flex-col items-center justify-center">
            <h1 className="text-5xl">Coming soon</h1>
            <div className="mt-10">
                <CompleteButton text="Exit" />
            </div>
        </FormWrapper>
    )
}
