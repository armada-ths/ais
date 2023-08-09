import PrimarySection from "./PrimarySection"
import { FormPageView } from "./FormPageView"
import { useSelector } from "react-redux"
import { selectActivePage } from "../../store/form/form_selectors"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"

export type FieldValue = string | boolean | undefined | File

export type Field = {
    mapping: string
    name: string
} & (
    | {
          type: "input-text"
          value?: string
      }
    | {
          type: "input-textarea"
          value?: string
      }
    | {
          type: "input-select"
          options: Array<{
              id: string
              text: string
          }>
          value?: string
      }
    | {
          type: "input-dropdown"
          options: Array<{
              id: string
              text: string
          }>
          value?: string
      }
    | {
          type: "input-switch"
          value?: boolean
      }
    | {
          type: "input-checkbox"
          value?: boolean
      }
    | {
          type: "text"
          text: string
      }
    | {
          type: "input-file"
          value?: File
      }
)

export interface FormPage {
    id: string
    title: string
    fields: Field[]
}

export interface Form {
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

    return (
        <div className="grid min-h-[100dvh] grid-cols-[1fr_3fr_1fr] grid-rows-[80px_1fr]">
            <div className="col-span-3 h-full bg-emerald-400"></div>
            <FormSidebarProgressionSummary />
            <PrimarySection>
                <div>
                    <h1 className="text-4xl">{form.name}</h1>
                    <FormPageView page={activePage} />
                </div>
            </PrimarySection>
            <div className="bg-blue-500" />
        </div>
    )
}
