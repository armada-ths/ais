import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useDates } from "@/shared/hooks/api/useDates"
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
        from: "/$companyId/form/$formKey/$formPageKey"
    })

    const { data: dataDates } = useDates()
    const { data, isLoading } = useDashboard()

    const [readTerms, setReadTerms] = useState(false)
    const [acceptedBinding, setAcceptedBinding] = useState(false)
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
    if (data == null || dataDates == null) {
        return <div>We encountered an error</div>
    }

    return (
        <div className="mt-6 flex max-w-[500px] flex-col items-center gap-y-5">
            <a href={`${HOST}${data?.ir_contract.contract}`} target="_blank">
                <Button variant={"outline"}>
                    Open Armada {DateTime.now().year} Exhibitor Contract
                </Button>
            </a>
            <div className="mt-6 flex items-center space-x-4">
                <Checkbox
                    id="read"
                    checked={readTerms}
                    onCheckedChange={x =>
                        x != "indeterminate" && setReadTerms(x)
                    }
                />
                <Label
                    htmlFor="read"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I have read and accepted the terms and conditions and
                    confirm that I have the right to enter this agreement on
                    behalf of <b>{data?.company.name}</b>
                </Label>
            </div>
            <div className="mt-6 flex items-center space-x-4">
                <Checkbox
                    id="binding"
                    checked={acceptedBinding}
                    onCheckedChange={x =>
                        x != "indeterminate" && setAcceptedBinding(x)
                    }
                />
                <Label
                    htmlFor="binding"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I understand that this Initial Registration is binding after{" "}
                    {DateTime.fromISO(dataDates.ir.acceptance).toFormat(
                        "yyyy MM dd"
                    )}{" "}
                    and have read the cancellation policy
                </Label>
            </div>
            <div className="mt-2 flex space-x-4">
                <Checkbox
                    id="process_data"
                    checked={processData}
                    onCheckedChange={x =>
                        x != "indeterminate" && setProcessData(x)
                    }
                />
                <Label
                    htmlFor="process_data"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I consent to letting THS Armada store my personal
                    information according to THS personal information policy
                </Label>
            </div>
            <div className="mt-5">
                {mutationIsSuccess ? (
                    <Button variant="link" onClick={exitView}>
                        Take the next step
                    </Button>
                ) : (
                    <Button
                        disabled={
                            !readTerms ||
                            !processData ||
                            !acceptedBinding ||
                            isPending
                        }
                        onClick={onClickSign}
                    >
                        Sign up as Exhibitor
                    </Button>
                )}
            </div>
        </div>
    )
}
