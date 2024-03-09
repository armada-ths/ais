import { Checkbox } from "primereact/checkbox"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { InputTextarea } from "primereact/inputtextarea"
import { MultiSelect, MultiSelectChangeEvent } from "primereact/multiselect"
import { SelectButton } from "primereact/selectbutton"
import React, { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import z from "zod"
import { FieldValue } from "../../forms/form_types"
import { HOST } from "../../shared/vars"
import { remoteSaveChanges } from "../../store/form/async_actions"
import { selectField, selectFieldErrors } from "../../store/form/form_selectors"
import { nextPage, setField } from "../../store/form/form_slice"
import { selectAdjustedProductPrice } from "../../store/products/products_selectors"
import { Product, pickProduct } from "../../store/products/products_slice"
import { AppDispatch, RootState } from "../../store/store"
import { cx } from "../../utils/cx"
import { formatCurrency } from "../../utils/format_currency"

export type FieldComponentProps = {
    label: string
    mapping: string
    readOnly?: boolean
    children?: React.ReactNode // Allow children in props
} & React.HTMLAttributes<HTMLDivElement>
export type FieldComponentType<T = FieldComponentProps> = (
    props: T
) => JSX.Element

function FormField() {
    return <div />
}

const TextInput: FieldComponentType<
    FieldComponentProps & {
        inputClassName?: string
    }
> = ({ label, mapping, readOnly, inputClassName, className, ...rest }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    const fieldErrors = useSelector((state: RootState) =>
        selectFieldErrors(state, mapping)
    )
    if (
        field == null ||
        (typeof field.value !== "string" && field.value != null)
    )
        return <div>Invalid field mapping</div>

    return (
        <span
            key={mapping}
            className={cx("p-float-label mt-8 basis-full", className)}
        >
            <InputText
                className={cx(
                    "w-full min-w-[200px] max-w-[600px]",
                    inputClassName,
                    !fieldErrors &&
                        field.value &&
                        "!border-2 !border-solid !border-slate-400",
                    fieldErrors && "p-invalid"
                )}
                readOnly={readOnly}
                value={field.value ?? ""}
                onChange={event =>
                    dispatch(
                        setField({
                            mapping,
                            value: event.target.value
                        })
                    )
                }
                {...rest}
            />
            <p className="mt-1 text-xs text-red-400">{fieldErrors?.error}</p>
            <label className="capitalize" htmlFor={mapping}>
                {label}
            </label>
        </span>
    )
}
FormField.Text = TextInput

const TextAreaInput: FieldComponentType = ({ label, mapping }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    const fieldErrors = useSelector((state: RootState) =>
        selectFieldErrors(state, mapping)
    )
    if (field?.value != null && typeof field.value !== "string")
        return <div>Invalid field mapping</div>

    return (
        <span key={mapping} className="flex flex-col">
            <label htmlFor={mapping}>{label}</label>
            <InputTextarea
                className={cx(
                    !fieldErrors &&
                        field?.value &&
                        "!border-2 !border-solid !border-slate-400",

                    fieldErrors && "p-invalid"
                )}
                id={mapping}
                name={mapping}
                value={field?.value ?? ""}
                onChange={event =>
                    dispatch(
                        setField({
                            mapping,
                            value: event.target.value
                        })
                    )
                }
            />
        </span>
    )
}
FormField.TextArea = TextAreaInput

const DropdownInput: FieldComponentType<
    FieldComponentProps & {
        options: { label: string; value: string }[]
    }
> = ({ label, mapping, options }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    if (field?.value == null || typeof field.value !== "string")
        return <div>Invalid field mapping</div>

    return (
        <span key={mapping} className="p-float-label">
            <Dropdown
                value={field.value ?? ""}
                options={options}
                onChange={event =>
                    dispatch(
                        setField({
                            mapping,
                            value: event.target.value
                        })
                    )
                }
            />
            <label htmlFor={mapping}>{label}</label>
        </span>
    )
}
FormField.Dropdown = DropdownInput

const CheckboxInput: FieldComponentType = ({ label, mapping }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    if (field?.value != null && typeof field.value !== "boolean")
        return <div>Invalid field mapping</div>

    return (
        <div className="flex items-center gap-5">
            <label>{label}</label>
            <Checkbox
                checked={field?.value ?? false}
                onChange={event =>
                    dispatch(
                        setField({
                            mapping,
                            value: event.target.checked
                        })
                    )
                }
            />
        </div>
    )
}
FormField.Checkbox = CheckboxInput

const SelectButtonInput: FieldComponentType<
    FieldComponentProps & {
        options: { label: string; value: string }[]
    }
> = ({ label, mapping, options }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    if (field?.value == null || typeof field.value !== "string")
        return <div>Invalid field mapping</div>

    return (
        <span key={mapping} className="p-float-label">
            <SelectButton
                value={field.value}
                options={options}
                onChange={event =>
                    dispatch(
                        setField({
                            mapping,
                            value: event.target.value
                        })
                    )
                }
            />
            <label htmlFor={mapping}>{label}</label>
        </span>
    )
}
FormField.SelectButton = SelectButtonInput

const MultiSelectInput: FieldComponentType<
    FieldComponentProps & {
        filter?: boolean
        optionLabel?: string
        optionValue?: string
    }
> = ({ mapping, label, className, filter, optionLabel, optionValue }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    const mapped =
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ((field?.value as unknown as FieldValue[]) ?? []).map((value: any) => ({
            id: value.id,
            label: value[optionLabel ?? "label"],
            selected: value[optionValue ?? "value"]
        })) ?? []

    const schema = z.array(
        z.object({ id: z.number(), label: z.string(), selected: z.boolean() })
    )
    const options = schema.parse(mapped)

    const [selected, setSelected] = useState(
        options.filter(option => option.selected).map(option => option.id)
    )

    useEffect(() => {
        if (field?.value == null || !Array.isArray(field.value)) return
        dispatch(
            setField({
                mapping,
                // eslint-disable-next-line @typescript-eslint/ban-ts-comment
                // @ts-ignore
                value: field?.value?.map(current => ({
                    ...(current as object),
                    selected:
                        selected?.find(
                            selected =>
                                selected ===
                                (current as unknown as { id: number }).id
                        ) != null
                })) as unknown as FieldValue // Casting here since values doesn't support objects (types)
            })
        )
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dispatch, selected])

    if (
        field?.value == null ||
        // Invalid if either field is not array or type is not set to allow multiple values
        !Array.isArray(field.value) ||
        !field.isMultiSelect
    ) {
        return <p>Invalid mapping for field "{mapping}"</p>
    }

    function setMultiField(event: MultiSelectChangeEvent) {
        setSelected(event.value)
    }

    return (
        <span className="p-float-label mt-8">
            <MultiSelect
                id={mapping}
                className={cx(
                    "[&>div>div]:flex [&>div>div]:flex-wrap [&>div>div]:gap-y-2 [&>div>div]:text-xs",
                    className
                )}
                filter={filter}
                display="chip"
                optionLabel="label"
                optionValue="id"
                value={selected}
                onChange={event => setMultiField(event)}
                options={options}
            />
            <label htmlFor={mapping}>{label}</label>
        </span>
    )
}
FormField.MultiSelect = MultiSelectInput

const PackageInput: FieldComponentType<
    FieldComponentProps & {
        product: Product
        children?: React.ReactNode
    }
> = ({ product, children }) => {
    const dispatch = useDispatch<AppDispatch>()
    const price = useSelector((state: RootState) =>
        selectAdjustedProductPrice(state, product.id)
    )

    async function onClickPackage() {
        dispatch(
            pickProduct({
                id: product.id,
                isPackage: true,
                quantity: 1
            })
        )
        dispatch(nextPage())
        // Force save changes to wait an itteration to make sure
        // previous dispatches are applied
        setTimeout(() => dispatch(remoteSaveChanges()))
    }

    return (
        <div
            className="flex w-72 select-none flex-col rounded-lg border-2 border-slate-500 transition-all duration-200 hover:cursor-pointer active:scale-95"
            onClick={onClickPackage}
        >
            <div>
                <h2 className="my-5 text-center text-xl text-slate-500">
                    {product.short_name || product.name}
                </h2>
                {children}
            </div>
            <div className="mx-5 h-0.5 bg-slate-500" />
            <div>
                {product.child_products.map(({ child_product, quantity }) => (
                    <div
                        key={child_product.id}
                        className="m-5 flex items-center gap-5 text-sm"
                    >
                        <i className="pi pi-check !font-bold text-emerald-400"></i>
                        <div className="flex gap-1 text-slate-500">
                            <p className="">
                                {child_product.short_name || child_product.name}
                            </p>
                            {quantity > 1 && <p> x {quantity}</p>}
                        </div>
                    </div>
                ))}
            </div>
            <div className="flex flex-1 items-end justify-center p-5">
                <p className="rounded bg-slate-500 p-1 px-3 text-center text-lg font-bold text-slate-50">
                    {formatCurrency(price)} kr
                </p>
            </div>
        </div>
    )
}
FormField.Package = PackageInput

const ImageInput: FieldComponentType<FieldComponentProps> = ({
    mapping,
    label
}) => {
    const dispatch = useDispatch()
    const image = useSelector((state: RootState) => selectField(state, mapping))
    if (image?.value != null && typeof image.value !== "string")
        return <p>Invalid field mapping</p>

    function convertBase64(file: File) {
        return new Promise((resolve, reject) => {
            const fileReader = new FileReader()
            fileReader.readAsDataURL(file)
            fileReader.onload = () => {
                resolve(fileReader.result)
            }
            fileReader.onerror = error => {
                reject(error)
            }
        })
    }

    async function onSubmitImage(event: React.ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0]
        if (file == null) return null
        const base64 = (await convertBase64(file)) as string
        dispatch(setField({ mapping, value: base64 }))
    }

    return (
        <div className="mt-5 grid grid-cols-2 gap-2">
            <p className="col-span-full">{label}</p>
            <div className="rounded bg-slate-100">
                {image?.value != null && (
                    <img
                        className="object-contain"
                        src={
                            image.value?.startsWith("data:")
                                ? image.value
                                : `${HOST}${image.value}`
                        }
                    />
                )}
            </div>
            <input
                type="file"
                onChange={onSubmitImage}
                className="flex h-full items-center justify-center rounded-lg border-2 border-dashed border-gray-700 bg-gray-100"
            />
        </div>
    )
}
FormField.Image = ImageInput

export { FormField }
