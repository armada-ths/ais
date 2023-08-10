import { Checkbox } from "primereact/checkbox"
import { InputText } from "primereact/inputtext"
import { InputTextarea } from "primereact/inputtextarea"
import { Dropdown } from "primereact/dropdown"
import { SelectButton } from "primereact/selectbutton"
import { useSelector } from "react-redux"
import { selectField } from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { useDispatch } from "react-redux"
import { nextPage, setField } from "../../store/form/form_slice"
import { cx } from "../../utils/cx"
import { Product, selectPackage } from "../../store/products/products_slice"

export type FieldComponentProps = {
    label: string
    mapping: string
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
> = ({ label, mapping, inputClassName, className, ...rest }) => {
    const dispatch = useDispatch()
    const field = useSelector((state: RootState) => selectField(state, mapping))
    if (
        field == null ||
        (typeof field.value !== "string" && field.value != null)
    )
        return <div>Invalid field mapping</div>

    console.log(className, "DING", rest)

    return (
        <span
            key={mapping}
            className={cx("p-float-label mt-8 basis-full", className)}
        >
            <InputText
                className={cx(
                    "mt-8 w-full min-w-[200px] max-w-[600px]",
                    inputClassName
                )}
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
    if (field?.value == null || typeof field.value !== "string")
        return <div>Invalid field mapping</div>

    return (
        <span key={mapping} className="p-float-label">
            <InputTextarea
                value={field.value ?? ""}
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
    if (field?.value == null || typeof field.value !== "boolean")
        return <div>Invalid field mapping</div>

    return (
        <span key={mapping} className="p-float-label">
            <Checkbox
                checked={field.value ?? false}
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

const PackageInput: FieldComponentType<
    FieldComponentProps & {
        product: Product
        children?: React.ReactNode
    }
> = ({ product, children }) => {
    const dispatch = useDispatch()

    function onClickPackage() {
        dispatch(selectPackage(product))
        dispatch(nextPage())
        console.log("CLICKED package")
    }

    return (
        <div
            className="flex w-72 select-none flex-col rounded-lg border-2 border-slate-500 transition-all duration-200 hover:cursor-pointer active:scale-95"
            onClick={onClickPackage}
        >
            <div>
                <h2 className="my-5 text-center text-xl text-slate-500">
                    {product.name}
                </h2>
                {children}
            </div>
            <div className="mx-5 h-0.5 bg-slate-500" />
            <div>
                {product.child_products.map(current => (
                    <div
                        key={current.id}
                        className="m-5 flex items-center gap-5"
                    >
                        <i className="pi pi-check !font-bold text-emerald-400"></i>
                        <p className="text-slate-500">{current.name}</p>
                    </div>
                ))}
            </div>
            <div className="flex flex-1 items-end justify-center p-5">
                <p className="rounded bg-slate-500 p-2 px-5 text-center text-2xl font-bold text-slate-50">
                    {product.unit_price} kr
                </p>
            </div>
        </div>
    )
}
FormField.Package = PackageInput

export { FormField }
