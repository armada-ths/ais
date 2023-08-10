import PrimarySection from "./PrimarySection"
import { FormPageView } from "./FormPageView"
import { useSelector } from "react-redux"
import {
    selectActivePage,
    selectActivePageIndex
} from "../../store/form/form_selectors"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"
import { cx } from "../../utils/cx"
import { RootState } from "../../store/store"
import { FormSidebarCartSummary } from "./sidebar/FormSidebarCartSummary"

export type FieldValue = string | boolean | undefined | File

export type Field = {
    mapping: string
    includeInProgressionSummary?: boolean
    readonly?: boolean
    value?: FieldValue
}

export interface FormPage {
    id: string
    title: string
    fields: Field[]
    hasNextButton?: boolean // If true, the page will have a next and previous button
    hasPrevButton?: boolean
    getProgress?: (state: RootState) => number // If a page has custom progress logic this can be used
}

export interface Form {
    key: string // The key field to map the form to the *.form.tsx
    name: string
    isSkippable: boolean
    description: string
    pages: FormPage[]
}

type Props = {
    form: Form
}

export function FormScreen({ form }: Props) {
    const activePage = useSelector(selectActivePage)
    const activePageIndex = useSelector(selectActivePageIndex)

    return (
        <div
            className={cx(
                "grid min-h-[100dvh] grid-cols-[1fr_3fr_1fr]",
                form.isSkippable && "grid-rows-[80px_1fr]"
            )}
        >
            {form.isSkippable && (
                <div className="col-span-3 h-full bg-emerald-400"></div>
            )}
            <FormSidebarProgressionSummary />
            <PrimarySection>
                <h1 className="border-b-2 border-solid border-slate-800 text-4xl">
                    {form.name}
                </h1>
                <FormPageView page={activePage} pageIndex={activePageIndex} />
            </PrimarySection>
            <FormSidebarCartSummary />
        </div>
    )
}
