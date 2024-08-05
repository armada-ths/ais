import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
    Drawer,
    DrawerContent,
    DrawerDescription,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger
} from "@/components/ui/drawer"
import { Label } from "@/components/ui/label"
import { FormIds } from "@/forms"
import { checkAccessDeclarations } from "@/forms/access_declaration_logic"
import { useAccessDeclaration } from "@/shared/hooks/api/useAccessDeclaration"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useDates } from "@/shared/hooks/api/useDates"
import { HOST } from "@/shared/vars"
import { cx } from "@/utils/cx"
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
    const accessDeclarationArgs = useAccessDeclaration()

    const [readTerms, setReadTerms] = useState(false)
    const [acceptedBinding, setAcceptedBinding] = useState(false)
    const [processData, setProcessData] = useState(false)

    const isFinalRegistration = checkAccessDeclarations(accessDeclarationArgs, [
        "complete_registration:::*:::*"
    ])

    const {
        mutate: signIr,
        isPending,
        isSuccess: mutationIsSuccess
    } = useMutation({
        mutationFn: async () =>
            await fetch(`${HOST}/api/dashboard/sign_ir`, {
                method: "POST"
            }),
        onSuccess: async response => {
            if (response.status < 200 || response.status >= 300)
                return toast.error("Failed to sign up")
            await queryClient.invalidateQueries({
                queryKey: ["dashboard"]
            })
            // Redirect back to the dashboard
            if (!isFinalRegistration) {
                toast.success("Signup complete", {
                    description: `You have successfully signed up for Armada ${
                        DateTime.now().year
                    }!`
                })
            }

            toast.success("First step done", {
                description: `You have completed the first step of the registration, continue to ordering ${
                    DateTime.now().year
                }!`
            })
        }
    })

    function exitView() {
        if (!isFinalRegistration) {
            navigate({
                to: "/$companyId",
                replace: true,
                params: { companyId }
            })

            return
        }

        navigate({
            to: "/$companyId/form/$formKey/$formPageKey",
            replace: true,
            params: {
                companyId,
                formKey: "fr_accounting" as FormIds,
                formPageKey: "packages"
            }
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

    const signupDisabled =
        !readTerms || !processData || !acceptedBinding || isPending

    const acceptanceDate = DateTime.fromISO(dataDates.ir.acceptance).toFormat(
        "d MMMM yyyy"
    )
    const frStartDate = DateTime.fromISO(dataDates.fr.start).toFormat(
        "d MMMM yyyy"
    )
    const frEndDate = DateTime.fromISO(dataDates.fr.end).toFormat("d MMMM yyyy")

    // const overfillWarning = (
    //     <>
    //         In order not to overfill the event, we will confirm your spot before{" "}
    //         {DateTime.fromISO(dataDates.ir.acceptance).toFormat("d MMMM")}.
    //     </>
    // )

    return (
        <div className="mt-6 flex max-w-[400px] flex-col items-center gap-y-5">
            <div className="rounded-lg bg-stone-200 p-2 px-4 ">
                <p className="my-3 text-xs text-stone-600">
                    Here you apply to participate in Armada{" "}
                    {DateTime.now().year}. {/* {overfillWarning} */}
                    Contact <a href="mailto:sales@armada.nu">
                        sales@armada.nu
                    </a>{" "}
                    if you have any questions
                </p>
            </div>
            <a href={`${HOST}${data?.ir_contract.contract}`} target="_blank">
                <Button variant={"outline"}>
                    Open Armada {DateTime.now().year} Terms and Conditions
                </Button>
            </a>
            <div className="mt-2 flex items-center space-x-4">
                <Checkbox
                    id="read"
                    checked={readTerms}
                    onCheckedChange={x =>
                        x != "indeterminate" && setReadTerms(x)
                    }
                />
                <Label
                    htmlFor="read"
                    className="text-sm font-medium leading-5 peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I have read and accept the Terms and Conditions, and confirm
                    that I have the right to enter this agreement on behalf of{" "}
                    <b>{data?.company.name}</b>
                </Label>
            </div>
            <div className="mt-2 flex items-center space-x-4">
                <Checkbox
                    id="binding"
                    checked={acceptedBinding}
                    onCheckedChange={x =>
                        x != "indeterminate" && setAcceptedBinding(x)
                    }
                />
                <Label
                    htmlFor="binding"
                    className="text-sm font-medium leading-5 peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I understand that this Initial Registration is binding after{" "}
                    {DateTime.fromISO(dataDates.ir.acceptance).toFormat(
                        "d MMMM yyyy"
                    )}{" "}
                    and have read the{" "}
                    <Drawer>
                        <DrawerTrigger className="underline hover:no-underline">
                            cancellation policy
                        </DrawerTrigger>
                        <DrawerContent className="mx-auto max-w-[500px] p-4">
                            <DrawerHeader>
                                <DrawerTitle>
                                    Initial Registration - Cancellation Policy
                                </DrawerTitle>
                                <DrawerDescription className="mt-5">
                                    <p className="italic">
                                        This is an excerpt from the terms and
                                        conditions (terms). In case of any
                                        differences between this and the terms,
                                        the terms apply.
                                    </p>
                                    <ul className="mt-4 list-disc space-y-1 px-3">
                                        <li>
                                            Cancellation before{" "}
                                            <b>{acceptanceDate}</b> is free of
                                            charge
                                        </li>
                                        <li>
                                            Cancellation after{" "}
                                            <b>{acceptanceDate}</b>, but before{" "}
                                            <b>{frStartDate}</b> costs 25% of a
                                            bronze kit
                                        </li>
                                        <li>
                                            Cancellation after{" "}
                                            <b>{frStartDate}</b>, but before{" "}
                                            <b>{frEndDate}</b> costs 75% of a
                                            bronze kit
                                        </li>
                                        <li>
                                            Cancellation after{" "}
                                            <b>{frEndDate}</b> costs the full
                                            price of any ordered products.
                                        </li>
                                    </ul>
                                </DrawerDescription>
                            </DrawerHeader>
                        </DrawerContent>
                    </Drawer>
                </Label>
            </div>
            <div className="mt-2 flex items-center space-x-4">
                <Checkbox
                    id="process_data"
                    checked={processData}
                    onCheckedChange={x =>
                        x != "indeterminate" && setProcessData(x)
                    }
                />
                <Label
                    htmlFor="process_data"
                    className="text-sm font-medium leading-5 peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    I consent to letting THS Armada store my personal
                    information according to THS personal information policy
                </Label>
            </div>
            <div className="mt-5">
                {mutationIsSuccess ? (
                    <Button variant="link" onClick={exitView}>
                        {isFinalRegistration
                            ? "Continue to ordering"
                            : "Take the next step"}
                    </Button>
                ) : (
                    <Button
                        disabled={signupDisabled}
                        className={cx("transition-all duration-200", {})}
                        onClick={onClickSign}
                    >
                        Sign up as Exhibitor
                    </Button>
                )}
            </div>
        </div>
    )
}
