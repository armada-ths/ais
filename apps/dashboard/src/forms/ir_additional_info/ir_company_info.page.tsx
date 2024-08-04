import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { FormWrapper } from "@/forms/FormWrapper"
import { useConfirmSaveAlert } from "@/shared/ConfirmSaveAlert"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { HOST } from "@/shared/vars"
import { asOptionalField } from "@/utils/zod_optional_field"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useBlocker, useParams } from "@tanstack/react-router"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"
const formSchema = z.object({
    orgName: z.string().min(2).max(50),
    identityNumber: z.string().min(2).max(50),
    website: asOptionalField(z.string().url()),
    corporateEmail: asOptionalField(z.string().email())
})

export default function IrAdditionalInfoPage() {
    const { companyId } = useParams({
        from: "/$companyId"
    })
    const queryClient = useQueryClient()
    const { data } = useDashboard()

    const [defaultValues, setDefaultValues] = useState<
        z.infer<typeof formSchema>
    >({
        orgName: data?.company.name ?? "",
        identityNumber: data?.company.identity_number ?? "",
        website: data?.company.website ?? "",
        corporateEmail: data?.company.general_email_address ?? ""
    })

    const { mutate, isPending } = useMutation({
        mutationFn: async ({
            orgName,
            identityNumber,
            website,
            corporateEmail
        }: z.infer<typeof formSchema>) =>
            fetch(`${HOST}/api/dashboard/`, {
                method: "PUT",
                body: JSON.stringify({
                    company: {
                        identity_number: identityNumber ?? null,
                        name: orgName ?? null,
                        general_email_address: corporateEmail ?? null,
                        website: website ?? null
                    }
                })
            }),
        onSuccess: async response => {
            if (response.status >= 200 || response.status < 300) {
                toast.success("Successfully updated")
            }
        }
    })

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues
    })

    const onSubmit = async (data: z.infer<typeof formSchema>) => {
        mutate(data)
        queryClient.invalidateQueries({
            queryKey: ["dashboard", companyId]
        })
        setDefaultValues(data)
        form.reset(data)
    }

    const { confirm } = useConfirmSaveAlert()
    useBlocker(confirm, form.formState.isDirty)

    return (
        <FormWrapper>
            <div className="flex max-w-md flex-col gap-y-4">
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="flex flex-col gap-y-10"
                    >
                        <FormField
                            name="orgName"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="org_name">
                                        Org Name*
                                    </FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Org Name"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Your company name
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            name="identityNumber"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="identity_number">
                                        Identity Number*
                                    </FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Identity Number"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        The company identity number (org.nr)
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            name="website"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="website">
                                        Website address
                                    </FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="https://example.com"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        The url to your company website
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            name="corporateEmail"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="corporateEmail">
                                        Corporate Email
                                    </FormLabel>
                                    <FormControl>
                                        <Input placeholder="Email" {...field} />
                                    </FormControl>
                                    <FormDescription>
                                        If available, please provide a
                                        non-personal e-mail address for future
                                        contact between Armada and your
                                        organization
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <div className="flex justify-center">
                            <Button type="submit" disabled={isPending}>
                                {isPending ? "Saving..." : "Save information"}
                            </Button>
                        </div>
                    </form>
                </Form>
            </div>
        </FormWrapper>
    )
}
