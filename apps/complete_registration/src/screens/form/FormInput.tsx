import { Checkbox } from "primereact/checkbox"
import { InputText } from "primereact/inputtext"
import { InputTextarea } from "primereact/inputtextarea"
import { Dropdown } from "primereact/dropdown"
import { SelectButton } from "primereact/selectbutton"
import { useSelector } from "react-redux"
import { selectField } from "../../store/form/form_selectors"
import { RootState } from "../../store/store"
import { useDispatch } from "react-redux"
import { setField } from "../../store/form/form_slice"
import { cx } from "../../utils/cx"

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
                    "mt-8 w-full min-w-[300px] max-w-[400px]",
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

const Filler = (props: React.HTMLAttributes<HTMLDivElement>) => {
    return <div className="flex-1 basis-2/5" {...props} />
}
FormField.Filler = Filler

export { FormField }
