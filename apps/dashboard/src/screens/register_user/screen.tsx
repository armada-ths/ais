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
import { toast } from "sonner"
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

    const companyId = params.companyId
    const companyName = params.companyName
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
                    method: "PUT",
                    body: JSON.stringify({
                        company:
                            companyId != null
                                ? null
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
                    error: "Could not create"
                }
            }
            return {
                error: null,
                data: (await response.json()) as z.infer<typeof formSchema>
            }
        }
    })

    async function onSubmit() {
        const response = await mutateAsync(form.getValues())
        if (response.error == null) {
            console.log("OUPS")
        }
        console.log("SUCCESS")
        toast.success("Succuessfully created account")
    }

    return (
        <div className="mx-auto max-w-xl px-4">
            <div>
                <h1
                    className={cx(
                        "my-4 text-center text-4xl font-bold text-melon-700 md:my-10 md:text-5xl"
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
                                    <Input placeholder="Password" {...field} />
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
