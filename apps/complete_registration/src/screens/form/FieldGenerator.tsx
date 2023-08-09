import { OldField } from "./screen"
import { InputText } from "primereact/inputtext"
import { Checkbox } from "primereact/checkbox"
import { InputTextarea } from "primereact/inputtextarea"
import { Dropdown } from "primereact/dropdown"
import { SelectButton } from "primereact/selectbutton"
import { useDispatch } from "react-redux"
import { setField } from "../../store/form/form_slice"

export default function FieldWrapper({ field }: { field: OldField }) {
    return (
        <div>
            <p>{field.name}</p>
            <FieldGenerator field={field} />
        </div>
    )
}

export function FieldGenerator({ field }: { field: OldField }) {
    const dispatch = useDispatch()

    function callSetField(value: string | boolean | File) {
        dispatch(
            setField({
                mapping: field.mapping,
                value
            })
        )
    }

    if (field.type === "input-text") {
        return (
            <InputText
                value={field.value ?? ""}
                placeholder={field.name}
                onChange={event => callSetField(event.target.value)}
            />
        )
    } else if (field.type === "input-checkbox") {
        return (
            <Checkbox
                checked={field.value ?? false}
                defaultChecked={false}
                onChange={event => callSetField(event.checked ?? false)}
            />
        )
    } else if (field.type === "input-textarea") {
        return (
            <InputTextarea
                value={field.value ?? ""}
                placeholder={field.name}
                onChange={event => callSetField(event.target.value)}
            />
        )
    } else if (field.type === "input-dropdown") {
        return (
            <Dropdown
                value={field.value}
                options={field.options.map(current => ({
                    label: current.text
                }))}
                onChange={event => callSetField(event.value)}
            />
        )
    } else if (field.type === "input-select") {
        return (
            <SelectButton
                value={field.value}
                options={field.options.map(current => ({
                    label: current.text
                }))}
                onChange={event => callSetField(event.value)}
            />
        )
    }
}
