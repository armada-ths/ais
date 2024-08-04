import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger
} from "@/components/ui/alert-dialog"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { HOST } from "@/shared/vars"
import { formatCurrency } from "@/utils/format_currency"
import { useNavigate, useParams } from "@tanstack/react-router"
import { ConfirmPopup } from "primereact/confirmpopup"
import { useState } from "react"
import { toast } from "sonner"

export function SummaryFormPage() {
    const { companyId } = useParams({
        from: "/$companyId/form/$formKey/$formPageKey"
    })
    const navigate = useNavigate()
    const [confirmTerms, setConfirmTerms] = useState<boolean>(false)
    const [confirmBinding, setConfirmBinding] = useState(false)
    const [confirmEligibility, setConfirmEligibility] = useState(false)

    const { data } = useDashboard()
    const { data: orders, isLoading: isLoadingOrders } = useOrders()
    const productPackage = orders.find(
        order => order.product.registration_section?.name.match(/package/i)
    )
    const company = data?.company

    const unfilledFields: Array<unknown> = []

    const readyToSign = confirmTerms && confirmBinding && confirmEligibility

    async function submitRegistration() {
        const response = await fetch(`${HOST}/api/dashboard/submit`, {
            method: "POST"
        })
        if (response.status < 200 || response.status >= 300) {
            toast.error("Error", {
                description:
                    "We encountered an error while submitting, if the problem persists please contact us."
            })
            return
        }

        navigate({
            to: "/$companyId",
            params: { companyId }
        })
    }

    const totalPrice = 0

    const grossPrice = formatCurrency(totalPrice * 1.25)

    if (isLoadingOrders) return null

    return (
        <div className="flex max-w-[450px] flex-col items-center">
            {(unfilledFields.length > 0 || productPackage == null) && (
                <h2 className="mb-2 text-lg text-red-400">
                    Missing information
                </h2>
            )}
            <div className="mb-5 flex gap-5">
                {productPackage == null ? (
                    <p className="mb-1 text-sm">No package selected</p>
                ) : (
                    <p className="mb-1 text-sm">
                        Make sure you have filled in your invoice information
                    </p>
                )}
                {/*                 {unfilledFields.map(current => (
                    <Card key={current.page.id}>
                        <h3 className="mb-2">{current.page.title}</h3>
                        {current.fields.map(field => (
                            <p key={field.mapping} className="mb-1 text-sm">
                                {field.mapping}
                            </p>
                        ))}
                    </Card>
                ))} */}
            </div>
            <div className="flex flex-col justify-center gap-4">
                <div className="flex items-center gap-x-5">
                    <Checkbox
                        id="terms-checkbox"
                        checked={confirmTerms}
                        className=""
                        onCheckedChange={value =>
                            setConfirmTerms(
                                value === "indeterminate" ? false : value
                            )
                        }
                    />
                    <Label htmlFor="terms-checkbox">
                        I have read and understand the{" "}
                        <a
                            className="font-medium text-melon-700 brightness-75 hover:underline dark:text-white"
                            href={data?.cr_contract.contract ?? ""}
                            target="_blank"
                        >
                            Armada Terms and Conditions.
                        </a>
                    </Label>
                </div>

                <div className="flex items-center gap-x-5">
                    <Checkbox
                        id="binding-checkbox"
                        checked={confirmBinding}
                        onCheckedChange={value =>
                            setConfirmBinding(
                                value === "indeterminate" ? false : value
                            )
                        }
                    />
                    <Label htmlFor="binding-checkbox" className="leading-tight">
                        I understand that the Final Registration is binding and{" "}
                        <i>{company?.name}</i> will be invoiced{" "}
                        <b>{grossPrice} kr</b> inc. VAT, by THS Armada, through
                        Tekniska Högskolans Studentkår, org. nr. 802005-9153
                    </Label>
                </div>

                <div className="flex items-center gap-x-5">
                    <Checkbox
                        id="eligibility-checkbox"
                        checked={confirmEligibility}
                        className=""
                        onCheckedChange={value =>
                            setConfirmEligibility(
                                value === "indeterminate" ? false : value
                            )
                        }
                    />
                    <Label htmlFor="eligibility-checkbox">
                        I have the authority to enter into this agreement on
                        behalf of <i>{company?.name}</i>
                    </Label>
                </div>
            </div>
            <div
                className="mt-10 text-justify text-xs text-stone-700"
                style={{ maxWidth: "50rem" }}
            >
                THS Armada will process any personal information you leave in
                this registration on the basis of legitimate interests. Your
                information will not be shared outside of THS (org. nr.
                802005-9153) and be used to provide you the services you order
                and to offer you similar services in the future. You are,
                according to GDPR, entitled to receive information regarding
                what personal data we process and how we process these. You also
                have the right to request a correction as to what personal data
                we are processing about you. To exercise these rights, contact
                a@armada.nu.
            </div>
            <div className="mt-8 flex justify-center">
                <ConfirmPopup />
                <div className="card justify-content-center flex flex-wrap gap-2 whitespace-nowrap">
                    <AlertDialog>
                        <AlertDialogTrigger asChild>
                            <Button disabled={!readyToSign}>
                                Confirm Final Registration
                            </Button>
                        </AlertDialogTrigger>
                        <AlertDialogContent>
                            <AlertDialogHeader>
                                <AlertDialogTitle>
                                    Final registration
                                </AlertDialogTitle>
                                <AlertDialogDescription>
                                    Have you filled in everything you want? Once
                                    your Final Registration has been made, you
                                    can no longer make changes without
                                    contacting us.
                                </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                                <AlertDialogCancel>Cancel</AlertDialogCancel>
                                <AlertDialogAction onClick={submitRegistration}>
                                    Complete registration
                                </AlertDialogAction>
                            </AlertDialogFooter>
                        </AlertDialogContent>
                    </AlertDialog>
                </div>
            </div>
        </div>
    )
}
