import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    InputErrorMessageText,
    InputLabel
} from "@/forms/components/input_label"
import { useConfirmSaveAlert } from "@/shared/ConfirmSaveAlert"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { HOST } from "@/shared/vars"
import { cn } from "@/utils/cx"
import { ErrorMessage } from "@hookform/error-message"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useBlocker, useParams } from "@tanstack/react-router"
import { Loader2Icon } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"
import { FormWrapper } from "../FormWrapper"

type InvoiceDetailsFormPageProps = {
    readOnly?: boolean
}

const formSchema = z.object({
    identity_number: z.string(),
    invoice_name: z.string().nonempty(),
    invoice_email_address: z.string().email(),
    invoice_address_line_1: z.string().nonempty(),
    invoice_address_line_2: z.string().nullable(),
    invoice_address_line_3: z.string().nullable(),
    invoice_zip_code: z.string().min(4).max(10),
    invoice_city: z.string().nonempty(),
    invoice_country: z.string().nonempty(),
    invoice_reference: z.string().nullable()
})

export function InvoiceDetailsFormPage({
    readOnly
}: InvoiceDetailsFormPageProps) {
    const { companyId } = useParams({
        from: "/$companyId/form/$formKey/$formPageKey"
    })

    const queryClient = useQueryClient()
    const { data } = useDashboard()

    const { mutate, isPending } = useMutation({
        mutationFn: async (data: z.infer<typeof formSchema>) =>
            fetch(`${HOST}/api/dashboard/${companyId}`, {
                method: "PUT",
                body: JSON.stringify({
                    company: data
                })
            }),
        onSuccess: async response => {
            if (response.status >= 200 && response.status < 300)
                toast.success("Invoice details updated")
            else {
                toast.error("Failed to update invoice details", {
                    description: JSON.stringify(await response.json())
                })
            }
        }
    })

    const [defaultFormValues, setDefaultFormValues] = useState<
        z.infer<typeof formSchema>
    >({
        identity_number: data?.company.identity_number as string,
        invoice_name: data?.company.invoice_name as string,
        invoice_email_address: data?.company.invoice_email_address as string,
        invoice_address_line_1: data?.company.invoice_address_line_1 as string,
        invoice_address_line_2: data?.company.invoice_address_line_2 ?? null,
        invoice_address_line_3: data?.company.invoice_address_line_3 ?? null,
        invoice_zip_code: data?.company.invoice_zip_code as string,
        invoice_city: data?.company.invoice_city as string,
        invoice_country: data?.company.invoice_country as string,
        invoice_reference: data?.company.invoice_reference ?? null
    })

    const {
        reset,
        register,
        handleSubmit,
        formState: { errors, isDirty }
    } = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: defaultFormValues
    })

    const { confirm } = useConfirmSaveAlert()
    useBlocker(confirm, isDirty)

    function onSubmit(data: z.infer<typeof formSchema>) {
        if (readOnly) return
        mutate(data)
        queryClient.invalidateQueries({
            queryKey: ["dashboard", companyId]
        })
        setDefaultFormValues(data)
        reset(data)
    }

    return (
        <FormWrapper>
            <form
                onSubmit={handleSubmit(onSubmit)}
                className="flex w-96 flex-col gap-4"
            >
                <div>
                    <InputLabel
                        htmlFor="identity-number"
                        tooltip="Your organization number"
                        required
                    >
                        Identity number
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="identity_number"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="identity-number"
                        {...register("identity_number")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="invoice-name"
                        tooltip="Name of organization"
                        required
                    >
                        Invoice name
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_name"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-name"
                        {...register("invoice_name")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="invoice-email"
                        tooltip="The email address of the person or entity that recieves the invoice"
                        required
                    >
                        Invoice email
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_email_address"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-email"
                        {...register("invoice_email_address")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="invoice-email-address"
                        tooltip="Address of billing organization"
                        required
                    >
                        Invoice address
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_address_line_1"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-address"
                        {...register("invoice_address_line_1")}
                    />
                </div>
                <div>
                    <InputLabel htmlFor="invoice-address-2">
                        Invoice address 2
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_address_line_2"
                        render={InputErrorMessageText}
                    />
                    <Input
                        disabled={readOnly}
                        id="invoice-address-2"
                        {...register("invoice_address_line_2")}
                    />
                </div>
                <div>
                    <InputLabel htmlFor="invoice-address-3">
                        Invoice address 3
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_address_line_3"
                        render={InputErrorMessageText}
                    />
                    <Input
                        disabled={readOnly}
                        id="invoice-address-3"
                        {...register("invoice_address_line_3")}
                    />
                </div>

                <div>
                    <InputLabel htmlFor="invoice-zip-code" required>
                        Invoice zip code
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_zip_code"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-zip-code"
                        {...register("invoice_zip_code")}
                    />
                </div>
                <div>
                    <InputLabel htmlFor="invoice-city" required>
                        Invoice city
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_city"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-city"
                        {...register("invoice_city")}
                    />
                </div>
                <div>
                    <InputLabel htmlFor="invoice-country" required>
                        Invoice country
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_country"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-country"
                        {...register("invoice_country")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="invoice-reference"
                        tooltip="Additional invoice information"
                    >
                        Invoice reference
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="invoice_reference"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        disabled={readOnly}
                        id="invoice-reference"
                        {...register("invoice_reference")}
                    />
                </div>
                {!readOnly && (
                    <Button type="submit" className={cn("flex gap-4")}>
                        {isPending && <Loader2Icon className="animate-spin" />}{" "}
                        Submit
                    </Button>
                )}
            </form>
        </FormWrapper>
    )
}
