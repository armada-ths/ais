import { FORMS } from "../forms"
import { FieldValue } from "../screens/form/screen"

export function mapToApi(forms: typeof FORMS) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const output = {} as any

    for (const formMeta of Object.values(forms)) {
        for (const page of formMeta.pages) {
            if (page.fields == null) continue
            for (const field of page.fields) {
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

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function reverseMap(parent: any) {
    const awaitingMappings: { mapping: string; value: FieldValue }[] = []
    for (const form of Object.values(FORMS)) {
        for (const page of form.pages) {
            for (const field of page.fields ?? []) {
                // Look for field in parent
                const path = field.mapping.split(".")
                let parentCopy = { ...parent }
                for (const part of path) {
                    if (parentCopy == null || parentCopy[part] === undefined)
                        continue

                    if (
                        part === path[path.length - 1] &&
                        parentCopy[part] != null &&
                        typeof parentCopy[part] !== "object"
                    ) {
                        awaitingMappings.push({
                            mapping: field.mapping,
                            value: parentCopy[part]
                        })
                        continue
                    }

                    parentCopy = parentCopy[part]
                }
            }
        }
    }
    return awaitingMappings
}
