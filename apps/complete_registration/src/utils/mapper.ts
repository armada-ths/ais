import { FieldValue, Form } from "../screens/form/screen"

export function mapToApi(form: Form) {
    const output = {} as any

    for (const page of form.pages) {
        for (const field of page.fields) {
            if (field.type === "text") continue
            map(field.mapping, output, field.value)
        }
    }
    return output
}

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

export function reverseMap(parent: any, form: Form) {
    const awaitingMappings: { mapping: string; value: FieldValue }[] = []
    for (const page of form.pages) {
        for (const field of page.fields) {
            if (field.type === "text") continue

            // Look for field in parent
            const path = field.mapping.split(".")
            console.log("PATH", path)
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

                console.log("Diving into", parentCopy, part)
                parentCopy = parentCopy[part]
            }
        }
    }
    console.log("MAPRESULT", awaitingMappings)
    return awaitingMappings
}
