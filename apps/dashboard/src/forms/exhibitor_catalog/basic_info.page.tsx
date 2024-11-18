import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
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
import { z, ZodType } from "zod"
import { FormWrapper } from "../FormWrapper"

const formSchema: ZodType = z.object({
    catalogue_about: z.string().max(600),
    catalogue_cities: z.string().optional().nullable(),
    catalogue_contact_name: z.string().optional().nullable(),
    catalogue_website_url: z.string().optional().nullable(),
    catalogue_contact_email_address: z.string().email().optional().nullable(),
    catalogue_contact_phone_number: z.string().max(20).optional().nullable()
})

export function BasicInfoFormPage() {
    const { companyId } = useParams({
        from: "/$companyId/*"
    })

    const queryClient = useQueryClient()
    const { data } = useDashboard()

    const [defaultFormValues, setDefaultFormValues] = useState<
        z.infer<typeof formSchema>
    >({
        catalogue_about: data?.exhibitor?.catalogue_about,
        catalogue_cities: data?.exhibitor?.catalogue_cities,
        catalogue_contact_name: data?.exhibitor?.catalogue_contact_name,
        catalogue_website_url: data?.company.website,
        catalogue_contact_email_address:
            data?.exhibitor?.catalogue_contact_email_address,
        catalogue_contact_phone_number:
            data?.exhibitor?.catalogue_contact_phone_number
    })

    const { mutate, isPending } = useMutation({
        mutationFn: async (data: z.infer<typeof formSchema>) => {
            const { catalogue_website_url, ...rest } = data

            return await fetch(`${HOST}/api/dashboard/${companyId}`, {
                method: "PUT",
                body: JSON.stringify({
                    company: {
                        website: catalogue_website_url ?? null
                    },
                    exhibitor: {
                        ...rest
                    }
                })
            })
        },
        onSuccess: response => {
            if (response.status >= 200 || response.status < 300) {
                toast.success("Successfully updated")
            }
        }
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

    function onSubmit(data: z.infer<typeof formSchema>) {
        mutate(data)
        queryClient.invalidateQueries({
            queryKey: ["dashboard", companyId]
        })
        setDefaultFormValues(data)
        reset(data)
    }

    const { confirm } = useConfirmSaveAlert()
    useBlocker(confirm, isDirty)

    return (
        <FormWrapper>
            <form
                onSubmit={handleSubmit(onSubmit)}
                className="flex w-96 flex-col gap-4"
            >
                <div>
                    <InputLabel
                        htmlFor="catalogue_about"
                        tooltip="Short description about your company"
                        required
                    >
                        About company
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="catalogue_about"
                        render={InputErrorMessageText}
                    />
                    <Textarea
                        tabIndex={1}
                        id="catalogue_about"
                        {...register("catalogue_about")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_cities"
                        tooltip="The cities where your company operates"
                    >
                        Catalogue cities
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="catalogue_cities"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        id="catalogue_cities"
                        {...register("catalogue_cities")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_contact_name"
                        tooltip="Company name"
                    >
                        Company name
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="catalogue_contact_name"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        id="catalogue_contact_name"
                        {...register("catalogue_contact_name")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_website_url"
                        tooltip="Company website"
                    >
                        Company website
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="catalogue_website_url"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        id="catalogue_website_url"
                        {...register("catalogue_website_url")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_contact_email_address"
                        tooltip="Email address to be publicly displayed"
                    >
                        Public email address
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="catalogue_contact_email_address"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        id="catalogue_contact_email_address"
                        {...register("catalogue_contact_email_address")}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_contact_email_address"
                        tooltip="Phone number to reach company at"
                    >
                        Public phone number
                    </InputLabel>
                    <ErrorMessage
                        errors={errors}
                        name="catalogue_contact_phone_number"
                        render={InputErrorMessageText}
                    />
                    <Input
                        tabIndex={1}
                        id="catalogue_contact_phone_number"
                        {...register("catalogue_contact_phone_number")}
                    />
                </div>
                <Button type="submit" className={cn("flex gap-4")}>
                    {isPending && <Loader2Icon className="animate-spin" />}{" "}
                    Submit and save
                </Button>
            </form>
        </FormWrapper>
    )
}
