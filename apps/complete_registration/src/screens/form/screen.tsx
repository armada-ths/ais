import PrimarySection from "./PrimarySection"
import { FormPageView } from "./FormPageView"
import { useSelector } from "react-redux"
import {
    selectActiveForm,
    selectActivePage,
    selectActivePageIndex
} from "../../store/form/form_selectors"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"
import { cx } from "../../utils/cx"
import { RootState } from "../../store/store"
import { FORMS } from "../../forms"
import { Navbar } from "../../shared/Navbar"

export type FieldValue = string | boolean | undefined | File

export type Field = {
    mapping: string
    mandatory?: boolean
    value?: FieldValue
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
    isSkippable: boolean
    description: string
    pages: FormPage[]
    rightSidebar?: () => JSX.Element
}

type Props = {
    form: Form
}

export function FormScreen({ form }: Props) {
    const activePage = useSelector(selectActivePage)
    const activePageIndex = useSelector(selectActivePageIndex)
    const activeForm = useSelector(selectActiveForm)

    if (activeForm == null || activePage == null) return <p>No form selected</p>

    return (
        <div>
            <Navbar />
            <div
                className={cx(
                    "grid min-h-[92vh] grid-cols-[1fr_3fr_1fr]",
                    form.isSkippable && "grid-rows-[80px_1fr]"
                )}
            >
                <FormSidebarProgressionSummary />
                <PrimarySection>
                    <FormPageView
                        form={activeForm}
                        page={activePage}
                        pageIndex={activePageIndex}
                    />
                </PrimarySection>
                {form.rightSidebar?.()}
            </div>
        </div>
    )
}
