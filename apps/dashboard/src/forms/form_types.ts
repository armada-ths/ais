import { DashboardResponse, Product } from "@/shared/hooks/useDashboard"

// eslint-disable-next-line @typescript-eslint/ban-types
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
    /**
     * @deprecated
     */
    fields?: Field[]
    hasNextButton?: boolean // If true, the page will have a next and previous button
    hasPrevButton?: boolean
    /**
     * @deprecated use isDone instead
     */
    getProgress?: (state: unknown) => number // If a page has custom progress logic this can be used
    isDone:
        | ((args: {
              form: Form
              registration: DashboardResponse
              products: Product[]
          }) => boolean)
        | null // If a page has custom done logic this can be used
    pageComponent: () => React.ReactNode
}

export interface Form {
    key: string // The key field to map the form to the *.form.tsx
    name: string
    forceFormDone?: boolean // The form will always be marked as done
    progression?: "none" | "silent" | "always" // none: no progression, silent: progression is shown but not included in company progress, always: progression is required, default is always
    description: string
    pages: FormPage[]
    rightSidebar?: () => JSX.Element
}
