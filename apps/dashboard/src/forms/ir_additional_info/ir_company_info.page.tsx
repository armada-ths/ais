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
import { useDashboard } from "@/shared/hooks/useRegistration"
import { HOST } from "@/shared/vars"
import { asOptionalField } from "@/utils/zod_optional_field"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { useForm } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"
const formSchema = z.object({
    orgName: z.string().min(2).max(50),
    identityNumber: z.string().min(2).max(50),
    website: asOptionalField(z.string().url().nullable()),
    corporateEmail: asOptionalField(z.string().email().nullable())
})

export default function IrAdditionalInfoPageWrapper() {
    const { data: dataRegistration, isLoading } = useDashboard()

    if (isLoading) return null
    if (!dataRegistration) return null

    return <IrAdditionalInfoPage dataRegistration={dataRegistration} />
}

export function IrAdditionalInfoPage({
    dataRegistration
}: {
    dataRegistration: NonNullable<
        Awaited<ReturnType<typeof useDashboard>>
    >["data"]
}) {
    const { mutateAsync } = useMutation({
        mutationFn: async ({
            orgName,
            identityNumber,
            website,
            corporateEmail
        }: z.infer<typeof formSchema>) => {
            const response = fetch(`${HOST}/api/dashboard/`, {
                method: "PUT",
                body: JSON.stringify({
                    company: {
                        identity_number: identityNumber,
                        name: orgName,
                        general_email_address: corporateEmail,
                        website
                    }
                })
            })
            return await (await response).json()
        }
    })

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            orgName: dataRegistration?.company.name ?? "",
            identityNumber: dataRegistration?.company.identity_number ?? "",
            website: dataRegistration?.company.website ?? "",
            corporateEmail:
                dataRegistration?.company.general_email_address ?? ""
        }
    })

    async function onSubmit(values: z.infer<typeof formSchema>) {
        console.log(values)
        await mutateAsync(values)
        toast.success("Information saved!")
    }

    return (
        <div className="flex max-w-md flex-col gap-y-4">
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="flex flex-col gap-y-10"
                >
                    <FormField
                        name="orgName"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="org_name">
                                    Org Name*
                                </FormLabel>
                                <FormControl>
                                    <Input placeholder="Org Name" {...field} />
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
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="corporateEmail">
                                    Corporate Email
                                </FormLabel>
                                <FormControl>
                                    <Input placeholder="Email" {...field} />
                                </FormControl>
                                <FormDescription>
                                    If available, please provide a non-personal
                                    e-mail address for future contact between
                                    Armada and your organization
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex justify-center">
                        <Button type="submit">Save information</Button>
                    </div>
                </form>
            </Form>
        </div>
    )
}
