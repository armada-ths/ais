/* eslint-disable @typescript-eslint/ban-ts-comment */
import { FORMS, getFieldFromForm } from "../forms"
import { FieldOption, FieldValue } from "../forms/form_types"

/**
 * @deprecated
 */
export function mapToApi(forms: typeof FORMS) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const output = {} as any

    for (const formMeta of Object.values(forms)) {
        for (const page of formMeta.pages) {
            // @ts-ignore
            if (page.fields == null) continue
            // @ts-ignore
            for (const field of page.fields) {
                if (Array.isArray(field.value)) {
                    mapValueOptions(
                        field.mapping,
                        output,
                        field.value as unknown as FieldOption[]
                    )
                    continue
                }

                map(field.mapping, output, field.value)
            }
        }
    }
    return output
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function map(mapping: string, parent: any, attachable: FieldValue) {
    const parts = mapping.split(".")
    let current = parent ?? {}

    for (const part of parts) {
        if (typeof current !== "object") continue
        if (current[part] === undefined) current[part] = {}

        if (part === parts[parts.length - 1]) current[part] = attachable

        current = current[part]
    }
}

export function mapValueOptions(
    mapping: string,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    parent: any,
    attachable: FieldOption[]
) {
    const parts = mapping.split(".")
    let current = parent ?? {}

    for (const part of parts) {
        if (typeof current !== "object") continue
        if (current[part] === undefined) current[part] = {}

        if (part === parts[parts.length - 1]) {
            current[part] = attachable
                .filter(current => current.selected)
                .map(current => ({
                    id: current.id
                }))
        }

        current = current[part]
    }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function reverseMap(parent: any) {
    const awaitingMappings: { mapping: string; value: FieldValue }[] = []
    for (const form of Object.values(FORMS)) {
        for (const page of form.pages) {
            // @ts-ignore
            for (const field of page.fields ?? []) {
                // Look for field in parent
                const path = field.mapping.split(".")
                let parentCopy = { ...parent }
                for (const part of path) {
                    if (parentCopy == null || parentCopy[part] === undefined) {
                        continue
                    }
                    if (
                        part === path[path.length - 1] &&
                        parentCopy[part] != null &&
                        (typeof parentCopy[part] !== "object" ||
                            Array.isArray(parentCopy[part]))
                    ) {
                        awaitingMappings.push({
                            mapping: field.mapping,
                            value: parentCopy[part]
                        })
                        continue
                    } else if (parentCopy[part] != null) {
                        const stateField = getFieldFromForm(
                            FORMS,
                            field.mapping
                        )
                        if (
                            // Make sure that array is end-node
                            stateField != null &&
                            stateField.isMultiSelect &&
                            Array.isArray(parentCopy[part])
                        ) {
                            awaitingMappings.push({
                                mapping: field.mapping,
                                value: parentCopy[part]
                            })
                            continue
                        }
                    }

                    parentCopy = parentCopy[part]
                }
            }
        }
    }
    return awaitingMappings
}
