import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { useDashboard } from "@/shared/hooks/useDashboard"
import { HOST } from "@/shared/vars"
import { queryClient } from "@/utils/query_client"
import { useMutation } from "@tanstack/react-query"
import { useNavigate, useParams } from "@tanstack/react-router"
import { DateTime } from "luxon"
import { useState } from "react"
import { toast } from "sonner"

export default function IrRegistrationPage() {
    const navigate = useNavigate()
    const { companyId } = useParams({
        from: "/$companyId/form/$formKey/$formStepKey"
    })
    const { data, isLoading } = useDashboard()

    const [terms, setTerms] = useState(false)
    const [processData, setProcessData] = useState(false)

    const {
        mutate: signIr,
        isPending,
        isSuccess: mutationIsSuccess
    } = useMutation({
        mutationFn: async () =>
            await fetch(`${HOST}/api/dashboard/sign_ir`, {
                method: "POST"
            }),
        onSuccess: async () => {
            await queryClient.invalidateQueries({
                queryKey: ["dashboard"]
            })
            // Redirect back to the dashboard
            toast.success("Signup complete", {
                description: `You have successfully signed up for Armada ${
                    DateTime.now().year
                }!`,
                onAutoClose: exitView,
                onDismiss: exitView
            })
        }
    })

    function exitView() {
        if (companyId == null) return
        // Redirect to the next step
        console.log("EXIT VIEW")
        navigate({
            to: "/$companyId/form/$formKey",
            replace: true,
            params: { companyId, formKey: "ir_additional_info" }
        })
    }

    function onClickSign() {
        signIr()
    }

    if (isLoading) {
        return <div>Loading...</div>
    }
    if (data == null) {
        return <div>We encountered an error</div>
    }

    return (
        <div className="mt-6 flex max-w-[700px] flex-col items-center gap-y-5">
            <a href={`${HOST}${data?.ir_contract.contract}`} target="_blank">
                <Button variant={"outline"}>
                    Open Armada {DateTime.now().year} Exhibitor Contract
                </Button>
            </a>
            <div className="mt-6 flex items-center space-x-4">
                <Checkbox
                    id="terms"
                    checked={terms}
                    onCheckedChange={x => x != "indeterminate" && setTerms(x)}
                />
                <label
                    htmlFor="terms"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I have read the binding contract and agree to terms, and I
                    am also authorized to register my organization for THS
                    Armada {DateTime.now().year} and sign this contract.*
                </label>
            </div>
            <div className="mt-2 flex space-x-4">
                <Checkbox
                    id="process_data"
                    checked={processData}
                    onCheckedChange={x =>
                        x != "indeterminate" && setProcessData(x)
                    }
                />
                <label
                    htmlFor="process_data"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    THS Armada would like to process personal data about you and
                    your organization to be able to contact you in conjunction
                    with complete registration and send you information
                    regarding the fair of {DateTime.now().year}. The data we
                    intend to collect and the process is forename, surname, the
                    title of your organization, phone number, and email address.
                    You decide for yourself if you want to leave any additional
                    information to us. The data will only be processed by the
                    project group in THS Armada and by THS Management. The data
                    will be saved in the Armada Internal Systems, AIS. You are,
                    according to GDPR (General Data Protection Regulation),
                    entitled to receive information regarding what personal data
                    we process and how we process these. You also have the right
                    to request a correction as to what personal data we are
                    processing about you. I consent for THS Armada to process my
                    personal data in accordance with the above.*
                </label>
            </div>
            <div className="mt-5">
                {mutationIsSuccess ? (
                    <Button variant="link" onClick={exitView}>
                        Take the next step
                    </Button>
                ) : (
                    <Button
                        disabled={!terms || !processData || isPending}
                        onClick={onClickSign}
                    >
                        Sign up as Exhibitor
                    </Button>
                )}
            </div>
        </div>
    )
}
