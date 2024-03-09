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
import { HOST } from "@/shared/vars"
import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import { useSearch } from "@tanstack/react-router"
import { cx } from "class-variance-authority"
import { useForm } from "react-hook-form"
import { z } from "zod"

const formSchema = z.object({
    firstName: z.string(),
    lastName: z.string(),
    email: z.string().email(),
    password: z.string()
})

export function RegisterCompanyUserScreen() {
    const params = useSearch({
        from: "/register_user"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
    }) as Record<string, string>

    const companyId = params.company_id
    const companyName = params.orgName
    const orgNumber = params.orgNumber

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema)
    })

    const { mutateAsync, isPending } = useMutation({
        mutationFn: async ({
            firstName,
            lastName,
            email,
            password
        }: z.infer<typeof formSchema>) => {
            const response = await fetch(
                `${HOST}/api/register/company_contact`,
                {
                    method: "POST",
                    body: JSON.stringify({
                        company: companyId
                            ? undefined
                            : {
                                  name: companyName,
                                  identity_number: orgNumber
                              },
                        contact: {
                            first_name: firstName ?? null,
                            last_name: lastName ?? null,
                            email_address: email ?? null,
                            company: companyId
                        },
                        password
                    })
                }
            )
            if (response.status !== 200) {
                return {
                    status: response.status,
                    error: "Could not create",
                    data: (await response.json()) as unknown
                }
            }
            return {
                status: response.status,
                error: null,
                data: (await response.json()) as z.infer<typeof formSchema>
            }
        }
    })

    async function onSubmit() {
        const response = await mutateAsync(form.getValues())
        if (response.status !== 200) {
            if (
                response.data != null &&
                typeof response.data === "object" &&
                "contact" in response.data &&
                response.data.contact != null &&
                typeof response.data.contact === "object" &&
                "email_address" in response.data.contact &&
                typeof response.data.contact.email_address === "string"
            ) {
                console.log("DING")
                form.setError("email", {
                    type: "value",
                    message: response.data.contact.email_address
                })
            }
        } else {
            // foce reload
            window.location.reload()
        }
    }

    return (
        <div className="mx-auto max-w-sm px-4">
            <div>
                <h1
                    className={cx(
                        "my-4 text-center text-4xl font-bold text-melon-700 md:my-10"
                    )}
                >
                    Create your account
                </h1>
            </div>
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="flex flex-col gap-y-4"
                >
                    <FormField
                        name="firstName"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="firstName">
                                    First name*
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="First name"
                                        {...field}
                                    />
                                </FormControl>
                                <FormDescription>
                                    Your first name
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        name="lastName"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="lastName">
                                    Last name*
                                </FormLabel>
                                <FormControl>
                                    <Input placeholder="Last name" {...field} />
                                </FormControl>
                                <FormDescription>Your surname</FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        name="email"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="email">Email*</FormLabel>
                                <FormControl>
                                    <Input placeholder="Email" {...field} />
                                </FormControl>
                                <FormDescription>
                                    Your personal email, if you have a corporate
                                    email you will be able to provide that later
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel htmlFor="password">
                                    Password*
                                </FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Password"
                                        type="password"
                                        {...field}
                                    />
                                </FormControl>
                                <FormDescription>
                                    Account password
                                </FormDescription>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex justify-center">
                        <Button type="submit" disabled={isPending}>
                            {isPending ? "Saving..." : "Create account"}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    )
}
