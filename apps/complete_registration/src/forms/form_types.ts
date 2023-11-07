import { FORMS } from "."
import { RootState } from "../store/store"

export type FieldValue = string | boolean | undefined | File | Object

export interface FieldOption {
    id: number
    label: string
    selected: boolean
}

export interface Field {
    mapping: string
    mandatory?: boolean
    isMultiSelect?: boolean
    multiSelectOptionMap?: never
    value?: FieldValue | FieldOption[]
}

export interface FormPage {
    id: string
    title: string
    fields?: Field[]
    hasNextButton?: boolean // If true, the page will have a next and previous button
    hasPrevButton?: boolean
    getProgress?: (state: RootState) => number // If a page has custom progress logic this can be used
    pageComponent: () => JSX.Element
}

export interface Form {
    key: keyof typeof FORMS // The key field to map the form to the *.form.tsx
    name: string
    forceFormDone?: boolean // The form will always be marked as done
    progression?: "none" | "silent" | "always" // none: no progression, silent: progression is shown but not included in company progress, always: progression is required, default is always
    description: string
    pages: FormPage[]
    rightSidebar?: () => JSX.Element
}
