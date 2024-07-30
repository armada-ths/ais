import { cx } from "@/utils/cx"
import {
    MultiSelectChangeEvent,
    MultiSelect as PMultiSelect
} from "primereact/multiselect"

export function MultiSelect<TValue, TOptions>({
    id,
    value,
    options,
    optionLabel,
    placeholder,
    onChange,
    onBlur,
    children
}: {
    id: string
    value: TValue
    options: TOptions[]
    optionLabel: string
    placeholder: string
    onChange: (event: MultiSelectChangeEvent) => void
    onBlur: (event: unknown) => void
    children?: React.ReactNode
}) {
    return (
        <PMultiSelect
            className={cx(
                "w-full [&>div>div]:flex [&>div>div]:flex-wrap [&>div>div]:gap-y-2 [&>div>div]:text-xs"
            )}
            display="chip"
            id={id}
            optionLabel={optionLabel}
            placeholder={placeholder}
            options={options}
            value={value}
            onChange={onChange}
            onBlur={onBlur}
        >
            {children}
        </PMultiSelect>
    )
}
