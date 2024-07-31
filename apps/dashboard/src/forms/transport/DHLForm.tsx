import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTrigger
} from "@/components/ui/dialog"
import { FormField } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger
} from "@/components/ui/tooltip"
import { useConfirmSaveAlert } from "@/shared/ConfirmSaveAlert"
import {
    DashboardResponse,
    useDashboard
} from "@/shared/hooks/api/useDashboard"
import { cn } from "@/utils/cx"
import { ErrorMessage } from "@hookform/error-message"
import { zodResolver } from "@hookform/resolvers/zod"
import { useBlocker } from "@tanstack/react-router"
import { InfoIcon } from "lucide-react"
import { useRef } from "react"
import { ControllerRenderProps, useForm } from "react-hook-form"
import { useReactToPrint } from "react-to-print"
import { z } from "zod"

// https://drive.google.com/file/d/1op7D51O0QpOljNQMBP-UscNRpWlRs31X/view?usp=drive_linkhttps://drive.google.com/file/d/1op7D51O0QpOljNQMBP-UscNRpWlRs31X/view?usp=drive_link

const PackageTypes = {
    TWO_PACKAGES: {
        description: (
            <>
                Two packages, max dimensions per package: 150x50x50 cm and max
                weight 35kg (e.g. roll up)
            </>
        ),
        maxPackages: 2
    },
    ONE_HALF_PALLET: {
        description: (
            <>One Half pallet max dimensions 60x50x150cm, max weight 400 kg</>
        ),
        maxPackages: 1
    },
    ONE_EURO_PALLET: {
        description: (
            <>
                One Euro pallet max dimensions 120x80x200cm, max weight 950 kg
                (e.g. counter case)
            </>
        ),
        maxPackages: 1
    },
    ONE_CAGE_TROLLEY: {
        description: (
            <>
                One Cage Trolley max dimensions 120x80x200cm max weight 950 kg
                (Cage Trolley is not provided by DHL)
            </>
        ),
        maxPackages: 1
    },
    ONE_CUSTOM: {
        description: <>Request outside the above options</>,
        maxPackages: 2
    }
}

const otherCompanySchema = z.object({
    company_name: z.string().min(1, { message: "Company name is required" }),
    address: z.string().min(1, { message: "Address is required" }),
    postal_code: z.string().min(1, { message: "Postal code is required" }),
    city: z.string().min(1, { message: "City is required" }),
    country: z.string().min(1, { message: "Country is required" }),
    contact_person: z
        .string()
        .min(1, { message: "Contact person is required" }),
    contact_person_tel: z
        .string()
        .min(1, { message: "Contact person telephone is required" }),
    open_office_hours: z.string().optional()
})

const formSchema = z.object({
    return_after_fair: z.enum(["yes", "no"]).default("no"),
    company_name: z.string().min(1, { message: "Company name is required" }),
    address: z.string().min(1, { message: "Address is required" }),
    postal_code: z.string().min(1, { message: "Postal code is required" }),
    city: z.string().min(1, { message: "City is required" }),
    country: z.string().min(1, { message: "Country is required" }),
    contact_person: z
        .string()
        .min(1, { message: "Contact person is required" }),
    contact_person_tel: z
        .string()
        .min(1, { message: "Contact person telephone is required" }),
    open_office_hours: z.string().optional(),
    org_nr: z.string().optional(),

    other_company: z.union([otherCompanySchema, z.undefined()]),

    package_type: z.enum(Object.keys(PackageTypes) as [string, ...string[]]),
    packages: z.array(
        z.object({
            length: z.number({
                invalid_type_error: "Length must be provided"
            }),
            width: z.number({
                invalid_type_error: "Width must be provided"
            }),
            height: z.number({
                invalid_type_error: "Height must be provided"
            }),
            weight: z.number({
                invalid_type_error: "Weight must be provided"
            }),
            stackable: z.enum(["yes", "no"])
        })
    )
})

function PrintablePDF({
    innerRef,
    data
}: {
    innerRef: React.RefObject<HTMLDivElement>
    data: z.infer<typeof formSchema>
}) {
    console.log({ data })

    return (
        <div ref={innerRef} className="only-print mx-auto mt-20 max-w-xl">
            <div className="mb-8 flex justify-around gap-2">
                <img
                    src="https://ais.armada.nu/static/images/DHL_rgb.png"
                    className="w-1/3"
                />
                <img
                    src="https://ais.armada.nu/static/images/THS_armada_logga.png"
                    className="w-1/3"
                />
            </div>
            <div>
                <h1 className="text-3xl">Pick up</h1>
                <table className="mb-4 mt-4 w-full border-collapse border-2 border-black">
                    <tbody>
                        <tr>
                            <td>Company name:</td>
                            <td>{data.company_name}</td>
                        </tr>
                        <tr>
                            <td>Address:</td>
                            <td>{data.address}</td>
                        </tr>
                        <tr>
                            <td>Postal Code</td>
                            <td>{data.postal_code}</td>
                        </tr>
                        <tr>
                            <td>City, Country</td>
                            <td>
                                {data.city} {data.country}
                            </td>
                        </tr>
                        <tr>
                            <td>Contact person</td>
                            <td>
                                {data.contact_person}. Tel:{" "}
                                {data.contact_person_tel}
                            </td>
                        </tr>
                        <tr>
                            <td>Orgnr:</td>
                            <td>{data.org_nr}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div>
                <h1 className="text-3xl">Return after the fair:</h1>
                <table className="mb-4 mt-4 w-full max-w-xs border-collapse border-2 border-black">
                    <tbody>
                        <tr>
                            <td>Yes</td>
                            <td>{data.return_after_fair === "yes" && "X"}</td>
                            <td>No</td>
                            <td>{data.return_after_fair === "no" && "X"}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div>
                <h1 className="text-3xl">
                    Please fill in and choose one of the following options:
                </h1>
                <table className="mb-4 mt-4 w-full border-collapse border-2 border-black">
                    <tbody>
                        <tr
                            className="border-2 border-black
                    "
                        >
                            <td colSpan={6}>
                                Two packages, max dimensions per package:
                                150x50x50 cm and max weight 35kg (e.g. roll up)
                            </td>
                        </tr>
                        <tr>
                            <td className="border-2 border-black">
                                Length (cm)
                            </td>
                            <td className="border-2 border-black">
                                Width (cm)
                            </td>
                            <td className="border-2 border-black">
                                Height (cm)
                            </td>
                            <td className="border-2 border-black">
                                Weight (kg)
                            </td>
                            <td className="border-2 border-black">
                                Stackable (yes/no)
                            </td>
                        </tr>
                        <tr>
                            <td className="border-2 border-black">&#8203;</td>
                            <td className="border-2 border-black"></td>
                            <td className="border-2 border-black"></td>
                            <td className="border-2 border-black"></td>
                            <td className="border-2 border-black"></td>
                        </tr>
                        <tr>
                            <td className="border-2 border-black">&#8203;</td>
                            <td className="border-2 border-black"></td>
                            <td className="border-2 border-black"></td>
                            <td className="border-2 border-black"></td>
                            <td className="border-2 border-black"></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {data.other_company && (
                <div>
                    <h1 className="text-3xl">
                        Return to a different address than pick-up:
                    </h1>
                    <table className="mb-4 mt-4 w-full border-collapse border-2 border-black">
                        <tr>
                            <td>Company name:</td>
                            <td>{data.other_company.company_name}</td>
                        </tr>
                        <tr>
                            <td>Address:</td>
                            <td>{data.other_company.address}</td>
                        </tr>
                        <tr>
                            <td>Postal Code</td>
                            <td>{data.other_company.postal_code}</td>
                        </tr>
                        <tr>
                            <td>City, Country</td>
                            <td>
                                {data.other_company.city}{" "}
                                {data.other_company.country}
                            </td>
                        </tr>
                        <tr>
                            <td>Contact person</td>
                            <td>
                                {data.other_company.contact_person}. Tel:{" "}
                                {data.other_company.contact_person_tel}
                            </td>
                        </tr>
                        {data.other_company.open_office_hours && (
                            <tr>
                                <td>Open office hours</td>
                                <td>{data.other_company.open_office_hours}</td>
                            </tr>
                        )}
                    </table>
                </div>
            )}
            <div className="text-xs text-slate-600">
                If "Request outside the above options" is filled, DHL will
                return to you with a price/quotation proposal.
            </div>
        </div>
    )
}

function InputLabel({
    children,
    htmlFor,
    required,
    tooltip
}: {
    children: React.ReactNode
    htmlFor: string
    required?: boolean
    tooltip?: string
}) {
    return (
        <div className="mb-1 flex gap-2 py-1">
            <Label
                htmlFor={htmlFor}
                className={cn("flex items-center gap-2", {
                    "font-thin": !required
                })}
            >
                {children}
                {!required && <p className="text-xs">(optional)</p>}
            </Label>
            {tooltip != null && (
                <Tooltip>
                    <TooltipTrigger type="button">
                        <InfoIcon size={15} />
                    </TooltipTrigger>
                    <TooltipContent>
                        <p className="text-sm">{tooltip}</p>
                    </TooltipContent>
                </Tooltip>
            )}
        </div>
    )
}

function InputErrorMessageText({ message }: { message: string }) {
    return <p className="text-xs text-red-500">{message}</p>
}

type CompanyInformationElement<T> = {
    field: T
    label: string
    tooltip?: string
    required: boolean
    type: "text" | "tel"
}

const OtherCompanyInformation: CompanyInformationElement<
    keyof z.infer<typeof otherCompanySchema>
>[] = [
    {
        field: "company_name",
        label: "Company name",
        required: true,
        type: "text"
    },
    {
        field: "address",
        label: "Address",
        required: true,
        type: "text"
    },
    {
        field: "postal_code",
        label: "Postal code",
        required: true,
        type: "text"
    },
    {
        field: "city",
        label: "City",
        required: true,
        type: "text"
    },
    {
        field: "country",
        label: "Country",
        required: true,
        type: "text"
    },
    {
        field: "contact_person",
        label: "Contact person",
        required: true,
        type: "text"
    },
    {
        field: "contact_person_tel",
        label: "Contact person telephone",
        required: true,
        type: "tel"
    },
    {
        field: "open_office_hours",
        label: "Open office hours",
        required: false,
        type: "text"
    }
]

const CompanyInformation: CompanyInformationElement<
    keyof z.infer<typeof formSchema>
>[] = [
    ...OtherCompanyInformation,
    {
        field: "org_nr",
        label: "Orgnr",
        required: false,
        type: "text"
    }
]

function DHLFilloutForm({ dashboard }: { dashboard: DashboardResponse }) {
    const ref = useRef(null)

    const companyName = dashboard.company.name.replace(/[^a-z0-9]/gi, "_")

    const handlePrint = useReactToPrint({
        content: () => ref.current,
        documentTitle: `${companyName}-DHL-Form.pdf`,
        removeAfterPrint: true
    })

    const {
        getValues,
        control,
        register,
        handleSubmit,
        setValue,
        formState: { errors, isDirty }
    } = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            return_after_fair: "no",
            company_name: dashboard.company.name ?? "",
            address:
                (dashboard.company.invoice_address_line_1 ||
                    dashboard.company.invoice_address_line_2 ||
                    dashboard.company.invoice_address_line_3) ??
                "",
            postal_code: dashboard.company.invoice_zip_code ?? "",
            city: dashboard.company.invoice_city ?? "",
            country: dashboard.company.invoice_country ?? "",
            contact_person: `${dashboard.contact?.first_name} ${dashboard.contact?.last_name}`,
            contact_person_tel:
                (dashboard.contact?.work_phone_number ||
                    dashboard.contact?.mobile_phone_number) ??
                "",
            org_nr: dashboard.company.identity_number,
            packages: []
        }
    })
    const { confirm } = useConfirmSaveAlert()
    useBlocker(confirm, isDirty)

    console.log({ errors })

    const otherCompanyForm = (
        otherCompanyField: ControllerRenderProps<
            z.infer<typeof formSchema>,
            "other_company"
        >
    ) => (
        <div>
            <>
                <div className="mb-3">
                    <InputLabel
                        htmlFor="other_company"
                        tooltip="Return to a different address than pick-up"
                        required
                    >
                        Return to a different address than pick-up
                    </InputLabel>
                    <Select
                        onValueChange={v =>
                            otherCompanyField.onChange(
                                v === "yes" ? {} : undefined
                            )
                        }
                        defaultValue={otherCompanyField.value ? "yes" : "no"}
                    >
                        <SelectTrigger>
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectGroup>
                                <SelectItem value="yes">Yes</SelectItem>
                                <SelectItem value="no">No</SelectItem>
                            </SelectGroup>
                        </SelectContent>
                    </Select>
                </div>
                {otherCompanyField.value && (
                    <Card>
                        <CardHeader>
                            <div className="flex items-center gap-2">
                                <span>
                                    Return to a different address than pick-up
                                </span>
                            </div>
                        </CardHeader>

                        <CardContent>
                            {OtherCompanyInformation.map(information => ({
                                ...information,
                                field: `other_company.${information.field}` as `other_company.${keyof z.infer<
                                    typeof otherCompanySchema
                                >}`
                            })).map(
                                ({ field, label, tooltip, required, type }) => (
                                    <div key={field} className="mb-2">
                                        <InputLabel
                                            htmlFor={field}
                                            tooltip={tooltip}
                                            required={required}
                                        >
                                            {label}
                                        </InputLabel>
                                        <Input
                                            type={type}
                                            id={field}
                                            {...register(field)}
                                        />
                                        <ErrorMessage
                                            errors={errors}
                                            name={field}
                                            render={InputErrorMessageText}
                                        />
                                    </div>
                                )
                            )}
                        </CardContent>
                    </Card>
                )}
            </>
        </div>
    )

    return (
        <>
            <PrintablePDF innerRef={ref} data={getValues()} />

            <form
                onSubmit={handleSubmit(() => handlePrint())}
                className="flex flex-col gap-4"
            >
                <Card>
                    <CardHeader>Company information</CardHeader>
                    <CardContent>
                        {CompanyInformation.map(
                            ({ field, label, tooltip, required, type }) => (
                                <div key={field} className="mb-2">
                                    <InputLabel
                                        htmlFor={field}
                                        tooltip={tooltip}
                                        required={required}
                                    >
                                        {label}
                                    </InputLabel>
                                    <Input
                                        type={type}
                                        tabIndex={1}
                                        id={field}
                                        {...register(field)}
                                    />
                                    <ErrorMessage
                                        errors={errors}
                                        name={field}
                                        render={InputErrorMessageText}
                                    />
                                </div>
                            )
                        )}
                    </CardContent>
                </Card>

                <FormField
                    control={control}
                    name="other_company"
                    render={({ field: otherCompanyField }) => (
                        <FormField
                            control={control}
                            name="return_after_fair"
                            render={({ field }) => (
                                <div>
                                    <div className="mb-3">
                                        <InputLabel
                                            htmlFor="return-after-fair"
                                            tooltip="You want to return your items after the fair"
                                            required
                                        >
                                            Return after fair
                                        </InputLabel>
                                        <Select
                                            onValueChange={v => {
                                                field.onChange(v)
                                                if (v === "no") {
                                                    otherCompanyField.onChange(
                                                        undefined
                                                    )
                                                }
                                            }}
                                            defaultValue={field.value}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Return after fair" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectGroup>
                                                    <SelectItem value="yes">
                                                        Yes
                                                    </SelectItem>
                                                    <SelectItem value="no">
                                                        No
                                                    </SelectItem>
                                                </SelectGroup>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    {field.value === "yes" &&
                                        otherCompanyForm(otherCompanyField)}
                                </div>
                            )}
                        />
                    )}
                />

                <FormField
                    control={control}
                    name="packages"
                    render={({ field: packagesField }) => (
                        <>
                            <FormField
                                control={control}
                                name="package_type"
                                render={({ field: packagesTypeField }) => (
                                    <div>
                                        <InputLabel
                                            htmlFor="package_type"
                                            required
                                        >
                                            Please fill in and choose one of the
                                            following transport options
                                        </InputLabel>
                                        <Select
                                            onValueChange={v => {
                                                packagesTypeField.onChange(v)

                                                const maxPackages =
                                                    PackageTypes[
                                                        v as keyof typeof PackageTypes
                                                    ].maxPackages

                                                if (
                                                    packagesField.value
                                                        ?.length > maxPackages
                                                ) {
                                                    setValue(
                                                        "packages",
                                                        packagesField.value.slice(
                                                            0,
                                                            maxPackages
                                                        )
                                                    )
                                                } else if (
                                                    packagesField.value
                                                        ?.length < maxPackages
                                                ) {
                                                    console.log(
                                                        "adding",
                                                        packagesField.value,
                                                        maxPackages
                                                    )

                                                    setValue("packages", [
                                                        ...(packagesField.value ??
                                                            []),
                                                        ...Array.from(
                                                            {
                                                                length:
                                                                    maxPackages -
                                                                    (packagesField
                                                                        .value
                                                                        ?.length ??
                                                                        0)
                                                            },
                                                            // eslint-disable-next-line @typescript-eslint/no-explicit-any
                                                            () => ({}) as any
                                                        )
                                                    ])
                                                }
                                            }}
                                            defaultValue={
                                                packagesTypeField.value
                                            }
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select package type" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {Object.entries(
                                                    PackageTypes
                                                ).map(
                                                    ([
                                                        key,
                                                        { description }
                                                    ]) => (
                                                        <SelectGroup key={key}>
                                                            <SelectItem
                                                                value={key}
                                                            >
                                                                {description}
                                                            </SelectItem>
                                                        </SelectGroup>
                                                    )
                                                )}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                )}
                            />
                            <div className="flex flex-col gap-3">
                                {packagesField.value.map((_, index) => (
                                    <Card key={index}>
                                        <CardHeader>
                                            Package {index + 1}
                                        </CardHeader>
                                        <CardContent className="flex gap-2">
                                            <div className="mb-2">
                                                <InputLabel
                                                    htmlFor={`packages.${index}..length`}
                                                    required
                                                >
                                                    Length (cm)
                                                </InputLabel>
                                                <Input
                                                    type="number"
                                                    {...register(
                                                        `packages.${index}.length`,
                                                        {
                                                            valueAsNumber: true
                                                        }
                                                    )}
                                                />
                                                <ErrorMessage
                                                    errors={errors}
                                                    name={`packages.${index}.length`}
                                                    render={
                                                        InputErrorMessageText
                                                    }
                                                />
                                            </div>
                                            <div className="mb-2">
                                                <InputLabel
                                                    htmlFor={`packages[${index}].width`}
                                                    required
                                                >
                                                    Width (cm)
                                                </InputLabel>
                                                <Input
                                                    type="number"
                                                    {...register(
                                                        `packages.${index}.width`,
                                                        {
                                                            valueAsNumber: true
                                                        }
                                                    )}
                                                />
                                                <ErrorMessage
                                                    errors={errors}
                                                    name={`packages.${index}.width`}
                                                    render={
                                                        InputErrorMessageText
                                                    }
                                                />
                                            </div>
                                            <div className="mb-2">
                                                <InputLabel
                                                    htmlFor={`packages[${index}].height`}
                                                    required
                                                >
                                                    Height (cm)
                                                </InputLabel>
                                                <Input
                                                    type="number"
                                                    {...register(
                                                        `packages.${index}.height`,
                                                        {
                                                            valueAsNumber: true
                                                        }
                                                    )}
                                                />
                                                <ErrorMessage
                                                    errors={errors}
                                                    name={`packages.${index}.height`}
                                                    render={
                                                        InputErrorMessageText
                                                    }
                                                />
                                            </div>
                                            <div className="mb-2">
                                                <InputLabel
                                                    htmlFor={`packages[${index}].weight`}
                                                    required
                                                >
                                                    Weight (kg)
                                                </InputLabel>
                                                <Input
                                                    type="number"
                                                    {...register(
                                                        `packages.${index}.weight`,
                                                        {
                                                            valueAsNumber: true
                                                        }
                                                    )}
                                                />
                                                <ErrorMessage
                                                    errors={errors}
                                                    name={`packages.${index}.weight`}
                                                    render={
                                                        InputErrorMessageText
                                                    }
                                                />
                                            </div>
                                            <div className="mb-2">
                                                <InputLabel
                                                    htmlFor={`packages.${index}.stackable`}
                                                    required
                                                >
                                                    Stackable
                                                </InputLabel>
                                                <Select
                                                    onValueChange={v =>
                                                        register(
                                                            `packages.${index}.stackable`
                                                        ).onChange({
                                                            target: {
                                                                value: v
                                                            }
                                                        })
                                                    }
                                                    defaultValue={
                                                        getValues().packages[
                                                            index
                                                        ].stackable
                                                    }
                                                >
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Stackable" />
                                                    </SelectTrigger>
                                                    <SelectContent>
                                                        <SelectGroup>
                                                            <SelectItem value="yes">
                                                                Yes
                                                            </SelectItem>
                                                            <SelectItem value="no">
                                                                No
                                                            </SelectItem>
                                                        </SelectGroup>
                                                    </SelectContent>
                                                </Select>
                                                <ErrorMessage
                                                    errors={errors}
                                                    name={`packages.${index}.stackable`}
                                                    render={
                                                        InputErrorMessageText
                                                    }
                                                />
                                            </div>
                                        </CardContent>
                                    </Card>
                                ))}
                            </div>
                        </>
                    )}
                />

                <Button type="submit">Print</Button>
            </form>
        </>
    )
}

function DHLFormInner({ dashboard }: { dashboard: DashboardResponse }) {
    return (
        <div>
            <Dialog>
                <DialogTrigger asChild>
                    <Button>Complete and save form as PDF</Button>
                </DialogTrigger>
                <DialogContent
                    className="
                        max-h-full
                        max-w-2xl
                        overflow-y-auto
                        rounded-lg
                        bg-white
                        p-4
                        shadow-lg
                    "
                >
                    <DialogHeader>Fill out DHL form</DialogHeader>
                    <DHLFilloutForm dashboard={dashboard} />
                </DialogContent>
            </Dialog>
        </div>
    )
}

export function DHLForm() {
    const { data, isPending } = useDashboard()

    if (isPending) {
        return <div>Loading...</div>
    }

    if (!data) {
        return <div>Could not load dashboard</div>
    }

    return <DHLFormInner dashboard={data} />
}
