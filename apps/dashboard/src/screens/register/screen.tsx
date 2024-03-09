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
        company => company["Organization Name"] === selectedCompany
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
                Welcome to armada
            </h1>
            <div className="mx-auto mb-10 mt-10 flex max-h-screen max-w-xl flex-col flex-wrap justify-between gap-y-20 md:flex-row">
                <div className="flex flex-col items-center">
                    <h3 className="mb-2 text-center text-xl">
                        Find your company
                    </h3>

                    <ComboBox
                        placeholder="Search company..."
                        onSelect={x => setSelectedCompany(x)}
                        onChange={x => setSearch(x.target.value)}
                        options={
                            filteredCompanies?.map(
                                x => x["Organization Name"]
                            ) ?? []
                        }
                    />
                    {selectedCompany && (
                        <div className="mt-4 w-full max-w-[200px] rounded bg-stone-100 p-2">
                            <p>Selected company</p>
                            <p className="font-bold">{selectedCompany}</p>
                        </div>
                    )}
                    {selectedCompanyId && (
                        <Button
                            className="mt-4"
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
                            Continue <ArrowRight className="ml-2" size={20} />
                        </Button>
                    )}
                </div>
                <div className="flex flex-col items-center">
                    <h3 className="mb-2 text-center text-xl">
                        Register your company
                    </h3>
                    <div className="flex max-w-xs flex-col items-center">
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
                                <div className="flex justify-center">
                                    <Button type="submit">
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
