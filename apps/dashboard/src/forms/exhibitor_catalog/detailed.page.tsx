import { Button } from "@/components/ui/button"
import { InputLabel } from "@/forms/components/input_label"
import { MultiSelect } from "@/forms/components/multi_select"
import { FormWrapper } from "@/forms/FormWrapper"
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
import { Controller, useForm } from "react-hook-form"
import { toast } from "sonner"
import { z } from "zod"

const formSchema = z.object({
    catalogue_employments: z.array(
        z.object({
            id: z.number(),
            employment: z.string(),
            include_in_form: z.boolean(),
            selected: z.boolean()
        })
    ),
    catalogue_industries: z.array(
        z.object({
            id: z.number(),
            industry: z.string(),
            include_in_form: z.boolean(),
            category: z.number().nullable(),
            selected: z.boolean()
        })
    ),
    catalogue_locations: z.array(
        z.object({
            id: z.number(),
            location: z.string(),
            include_in_form: z.boolean(),
            selected: z.boolean()
        })
    )
})

export function DetailedFormPage() {
    const { companyId } = useParams({
        from: "/$companyId/*"
    })

    const queryClient = useQueryClient()
    const { data } = useDashboard()

    const [defaultData, setDefaultData] = useState<z.infer<typeof formSchema>>({
        catalogue_employments:
            data?.exhibitor?.catalogue_employments.filter(
                employment => employment.selected && employment.include_in_form
            ) ?? [],
        catalogue_industries:
            data?.exhibitor?.catalogue_industries.filter(
                industry => industry.selected && industry.include_in_form
            ) ?? [],
        catalogue_locations:
            data?.exhibitor?.catalogue_locations.filter(
                location => location.selected && location.include_in_form
            ) ?? []
    })

    const { mutate, isPending } = useMutation({
        mutationFn: async (data: z.infer<typeof formSchema>) =>
            await fetch(`${HOST}/api/dashboard/${companyId}`, {
                method: "PUT",
                body: JSON.stringify({
                    exhibitor: {
                        catalogue_employments: data.catalogue_employments.map(
                            employment => ({
                                id: employment.id,
                                selected: true
                            })
                        ),
                        catalogue_industries: data.catalogue_industries.map(
                            industry => ({
                                id: industry.id,
                                selected: true
                            })
                        ),
                        catalogue_locations: data.catalogue_locations.map(
                            location => {
                                return {
                                    id: location.id,
                                    selected: true
                                }
                            }
                        )
                    }
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

    const {
        reset,
        control,
        handleSubmit,
        formState: { errors, isDirty }
    } = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: defaultData
    })

    function onSubmit(data: z.infer<typeof formSchema>) {
        mutate(data)
        queryClient.invalidateQueries({
            queryKey: ["dashboard", companyId]
        })
        setDefaultData(data)
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
                        htmlFor="catalogue_employments"
                        tooltip="What employment opportunities are you offering"
                        required
                    >
                        Employment types
                    </InputLabel>
                    <ErrorMessage
                        name="catalogue_employments"
                        errors={errors}
                    />
                    <Controller
                        control={control}
                        name="catalogue_employments"
                        render={({ field }) => (
                            <MultiSelect
                                id="catalogue_employments"
                                optionLabel="employment"
                                placeholder="Select your employment types"
                                value={field.value}
                                options={
                                    data?.exhibitor?.catalogue_employments.filter(
                                        employment => employment.include_in_form
                                    ) ?? []
                                }
                                onChange={field.onChange}
                                onBlur={field.onBlur}
                            />
                        )}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_industries"
                        tooltip="What industries are you in"
                        required
                    >
                        Industries
                    </InputLabel>
                    <ErrorMessage name="catalogue_industries" errors={errors} />
                    <Controller
                        control={control}
                        name="catalogue_industries"
                        render={({ field }) => (
                            <MultiSelect
                                id="catalogue_industries"
                                optionLabel="industry"
                                placeholder="Select your industries"
                                options={
                                    data?.exhibitor?.catalogue_industries.filter(
                                        industry => industry.include_in_form
                                    ) ?? []
                                }
                                value={field.value}
                                onChange={field.onChange}
                                onBlur={field.onBlur}
                            />
                        )}
                    />
                </div>
                <div>
                    <InputLabel
                        htmlFor="catalogue_locations"
                        tooltip="Locations where your company operates"
                        required
                    >
                        Locations
                    </InputLabel>
                    <ErrorMessage name="catalogue_locations" errors={errors} />
                    <Controller
                        control={control}
                        name="catalogue_locations"
                        render={({ field }) => (
                            <MultiSelect
                                id="catalogue_locations"
                                optionLabel="location"
                                placeholder="Select your locations"
                                options={
                                    data?.exhibitor?.catalogue_locations.filter(
                                        location => location.include_in_form
                                    ) ?? []
                                }
                                value={field.value}
                                onChange={field.onChange}
                                onBlur={field.onBlur}
                            />
                        )}
                    />
                </div>

                <Button type="submit" className={cn("flex gap-4")}>
                    {isPending && <Loader2Icon className="animate-spin" />}{" "}
                    Submit
                </Button>
            </form>
            {/*             <FormField.MultiSelect
                label="Your industries (Think about everything an interesting student might search for)"
                mapping="exhibitor.catalogue_industries"
                className="w-full"
                filter
                optionLabel="industry"
                optionValue="selected"
            />
            <FormField.MultiSelect
                label="What employment are you offering?"
                mapping="exhibitor.catalogue_employments"
                className="w-full"
                filter
                optionLabel="employment"
                optionValue="selected"
            />
            <FormField.MultiSelect
                label="Select your countries"
                mapping="exhibitor.catalogue_locations"
                className="w-full"
                filter
                optionLabel="location"
                optionValue="selected"
            /> */}
        </FormWrapper>
    )
}
