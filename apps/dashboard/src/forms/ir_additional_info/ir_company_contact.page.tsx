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
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { debounce } from "@/shared/hooks/useDebounce"
import { HOST } from "@/shared/vars"
import { asOptionalField } from "@/utils/zod_optional_field"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

const formSchema = z.object({
    firstName: z.string().min(2).max(50),
    lastName: z.string().min(2).max(50),
    email: z.string().email(),
    alternativeEmail: asOptionalField(z.string().email().nullable()),
    title: asOptionalField(z.string().min(2).max(50).nullable()),
    mobileNumber: asOptionalField(z.string().min(2).max(50).nullable()),
    workPhoneNumber: asOptionalField(z.string().min(2).max(50).nullable())
})

export default function IrContactWrapper() {
    const { data: dataRegistration, isLoading } = useDashboard()

    if (isLoading) return null
    if (!dataRegistration) return null

    return <IrContactPage dataRegistration={dataRegistration} />
}

export function IrContactPage({
    dataRegistration
}: {
    dataRegistration: NonNullable<
        Awaited<ReturnType<typeof useDashboard>>
    >["data"]
}) {
    const { mutateAsync, isPending } = useMutation({
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
        }
    })

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            firstName: dataRegistration?.contact.first_name ?? "",
            lastName: dataRegistration?.contact.last_name ?? "",
            email: dataRegistration?.contact.email_address ?? "",
            alternativeEmail:
                dataRegistration?.contact.alternative_email_address ?? "",
            title: dataRegistration?.contact.title ?? "",
            mobileNumber: dataRegistration?.contact.mobile_phone_number ?? "",
            workPhoneNumber: dataRegistration?.contact.work_phone_number ?? ""
        }
    })

    async function onSubmit(values: z.infer<typeof formSchema>) {
        console.log("SUBMIT", values)
        await mutateAsync(values)
    }

    // Autosaving
    useEffect(() => {
        const subscriber = form.watch(
            debounce(() => form.handleSubmit(onSubmit)(), { delay: 1000 })
        )
        return () => subscriber.unsubscribe()
    })

    return (
        <div className="flex w-screen max-w-md flex-col">
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="flex flex-col gap-y-8"
                >
                    <FormField
                        name="firstName"
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
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="lastName">
                                    Surname*
                                </FormLabel>
                                <FormControl>
                                    <Input placeholder="Surname" {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex flex-col gap-y-2">
                        <FormField
                            name="email"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="website">
                                        Email*
                                    </FormLabel>
                                    <FormControl>
                                        <Input placeholder="Email" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            name="alternativeEmail"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel htmlFor="alternativeEmail">
                                        Alternative Email
                                    </FormLabel>
                                    <FormControl>
                                        <Input placeholder="Mail" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                    </div>
                    <FormField
                        name="title"
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
    )
}
