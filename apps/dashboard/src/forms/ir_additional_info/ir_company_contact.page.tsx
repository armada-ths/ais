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
    firstName: z.string().min(2).max(50),
    lastName: z.string().min(2).max(50),
    email: z.string().email(),
    alternativeEmail: asOptionalField(z.string().email()),
    title: asOptionalField(z.string().min(2).max(50)),
    mobileNumber: asOptionalField(z.string().min(2).max(50)),
    workPhoneNumber: asOptionalField(z.string().min(2).max(50))
})

export default function IrContactPage() {
    const { companyId } = useParams({
        from: "/$companyId"
    })
    const queryClient = useQueryClient()
    const { data } = useDashboard()

    const [defaultValues, setDefaultValues] = useState<
        z.infer<typeof formSchema>
    >({
        firstName: data?.contact?.first_name ?? "",
        lastName: data?.contact?.last_name ?? "",
        email: data?.contact?.email_address ?? "",
        alternativeEmail: data?.contact?.alternative_email_address ?? "",
        title: data?.contact?.title ?? "",
        mobileNumber: data?.contact?.mobile_phone_number ?? "",
        workPhoneNumber: data?.contact?.work_phone_number ?? ""
    })

    const { mutate, isPending } = useMutation({
        mutationFn: async ({
            firstName,
            lastName,
            email,
            alternativeEmail,
            title,
            mobileNumber,
            workPhoneNumber
        }: z.infer<typeof formSchema>) => {
            const response = fetch(`${HOST}/api/dashboard/`, {
                method: "PUT",
                body: JSON.stringify({
                    contact: {
                        first_name: firstName ?? null,
                        last_name: lastName ?? null,
                        email_address: email ?? null,
                        alternative_email_address: alternativeEmail ?? null,
                        title: title ?? null,
                        mobile_phone_number: mobileNumber ?? null,
                        work_phone_number: workPhoneNumber ?? null
                    }
                })
            })
            return await (await response).json()
        },
        onSuccess: data => {
            if ("error" in data) {
                toast.error("Failed to save changes", {
                    description: `Something did not work trying to save your contact information. Please try again or contact us. Error: ${data.error}`
                })
                return
            }
            toast.success("Saved changes", {
                description: "Your contact information has been saved!"
            })
        },
        onError: () => {
            toast.error("Failed to save changes", {
                description:
                    "Something did not work trying to save your contact information. Please try again or contact us."
            })
        }
    })

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues
    })

    async function onSubmit(data: z.infer<typeof formSchema>) {
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
            <div className="flex w-screen max-w-md flex-col">
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="flex flex-col gap-y-8"
                    >
                        <FormField
                            name="firstName"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="org_name">
                                        First Name*
                                    </FormLabel>
                                    <FormControl>
                                        <Input placeholder="Name" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            name="lastName"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="lastName">
                                        Surname*
                                    </FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Surname"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <div className="flex flex-col gap-y-2">
                            <FormField
                                name="email"
                                control={form.control}
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel htmlFor="website">
                                            Email*
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="Email"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                name="alternativeEmail"
                                control={form.control}
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel htmlFor="alternativeEmail">
                                            Alternative Email
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="Mail"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </div>
                        <FormField
                            name="title"
                            control={form.control}
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="title">Title</FormLabel>
                                    <FormControl>
                                        <Input placeholder="Title" {...field} />
                                    </FormControl>
                                    <FormDescription>Job title</FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <div className="flex flex-col gap-y-2">
                            <FormField
                                name="mobileNumber"
                                control={form.control}
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel htmlFor="mobileNumber">
                                            Mobile Number
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="Mobile Number"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                name="workPhoneNumber"
                                control={form.control}
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel htmlFor="workPhoneNumber">
                                            Work Phone Number
                                        </FormLabel>
                                        <FormControl>
                                            <Input
                                                placeholder="Work Phone Number"
                                                {...field}
                                            />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                        </div>
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
