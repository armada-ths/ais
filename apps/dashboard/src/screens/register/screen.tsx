import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
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
import { Separator } from "@/components/ui/separator"
import { useCompanies } from "@/shared/hooks/api/useCompanies"
import { zodResolver } from "@hookform/resolvers/zod"
import { useNavigate } from "@tanstack/react-router"
import { cx } from "class-variance-authority"
import { ArrowRight } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import ComboBox from "react-responsive-combo-box"
import "react-responsive-combo-box/dist/index.css"
import { z } from "zod"

const formSchema = z.object({
    orgName: z.string(),
    orgNumber: z.string()
})

export function RegisterScreen() {
    const navigate = useNavigate()
    const { data } = useCompanies()

    const [search, setSearch] = useState("")
    const [selectedCompany, setSelectedCompany] = useState("")
    const selectedCompanyId = data?.find(
        company =>
            selectedCompany && company["Organization Name"] === selectedCompany
    )?.id

    const filteredCompanies = data?.filter(
        company =>
            company["Organization Name"] &&
            company["Organization Name"]
                .toLowerCase()
                .includes(search.toLowerCase())
    )

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema)
    })

    async function onSubmit() {
        const values = form.getValues()
        console.log(values)

        navigate({
            from: "/register",
            to: `/register_user`,
            search: values
        })
    }

    return (
        <div>
            <h1
                className={cx(
                    "my-10 text-center text-4xl font-bold text-melon-700 md:my-10"
                )}
            >
                Armada Dashboard
            </h1>
            <div className="mx-auto mb-10 mt-10 flex max-h-screen max-w-xl flex-col-reverse flex-wrap items-center justify-between gap-y-20 md:flex-row md:items-start">
                <div className="flex max-w-xs flex-col items-center rounded-lg bg-stone-100 p-4 px-6">
                    <div className="mx-auto max-w-[200px] flex-col items-center">
                        <h3 className="text-center text-xl">
                            Find your company
                        </h3>
                        <Separator className="mb-4 mt-2" />

                        <p className="mx-auto mb-2 text-sm text-stone-600">
                            Have you been an exhibitor at Armada before?
                        </p>
                        <div className="flex flex-col md:hidden">
                            <Alert className="mt-2" variant={"destructive"}>
                                <AlertTitle>Mobile not supported</AlertTitle>
                                <AlertDescription>
                                    You cannot connect to an existing company on
                                    mobile
                                </AlertDescription>
                            </Alert>
                        </div>
                        <div className="hidden flex-col md:flex">
                            <ComboBox
                                placeholder="Select your company..."
                                style={{
                                    backgroundColor: "white",
                                    fontSize: "0.9rem"
                                }}
                                onSelect={x => setSelectedCompany(x)}
                                onChange={x => setSearch(x.target.value)}
                                options={
                                    filteredCompanies?.map(
                                        x => x["Organization Name"]
                                    ) ?? []
                                }
                            />
                            <Separator className="my-4" />
                            {selectedCompany && (
                                <div className="w-full rounded bg-stone-100">
                                    <p>Selected company</p>
                                    <p className="font-bold">
                                        {selectedCompany}
                                    </p>
                                </div>
                            )}
                            <div className="flex-1" />
                            <Button
                                disabled={selectedCompanyId == null}
                                className="mt-4 w-full"
                                onClick={() =>
                                    navigate({
                                        from: "/register",
                                        to: `/register_user`,
                                        search: {
                                            company_id: selectedCompanyId
                                        }
                                    })
                                }
                            >
                                Continue{" "}
                                <ArrowRight className="ml-2" size={20} />
                            </Button>
                        </div>
                    </div>
                </div>
                <div className="flex max-w-xs flex-col rounded-lg bg-stone-100 p-4 px-6">
                    <h3 className="mb-2 text-center text-xl">
                        Register your company
                    </h3>
                    <Separator className="mb-4 mt-2" />
                    <div className="flex max-w-[200px] flex-col">
                        <Form {...form}>
                            <form
                                onSubmit={form.handleSubmit(onSubmit)}
                                className="flex flex-col gap-y-4"
                            >
                                <FormField
                                    name="orgName"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor="orgName">
                                                Company Name*
                                            </FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="Company Name"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    name="orgNumber"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel htmlFor="orgNumber">
                                                Organization number*
                                            </FormLabel>
                                            <FormControl>
                                                <Input
                                                    placeholder="Org number"
                                                    {...field}
                                                />
                                            </FormControl>
                                            <FormDescription>
                                                (org.nr)
                                            </FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <div className="flex-1" />
                                <div className="flex justify-center">
                                    <Button type="submit" className="w-full">
                                        Continue{" "}
                                        <ArrowRight
                                            className="ml-2"
                                            size={20}
                                        />
                                    </Button>
                                </div>
                            </form>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    )
}
