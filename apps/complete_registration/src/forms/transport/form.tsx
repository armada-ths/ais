import { Form } from "../../screens/form/screen"
import { TransportSummaryFormPage } from "./summary.page"
import { TransportInfoFormPage } from "./transport_info.page"

export const form: Form = {
    key: "transport",
    name: "Armada Transport",
    description: "Armada transport system",
    isSkippable: false,
    pages: [
        {
            id: "transport_info",
            title: "Transport",
            pageComponent: TransportInfoFormPage,
            fields: [
                {
                    mapping: "exhibitor.transport_information_read"
                }
            ]
        },
        {
            id: "transport_summary",
            title: "Transport Summary",
            hasNextButton: false,
            hasPrevButton: false,
            pageComponent: TransportSummaryFormPage,
            fields: [
                {
                    mapping: "exhibitor.transport_to",
                    mandatory: false
                },
                {
                    mapping: "exhibitor.transport_from",
                    mandatory: false
                }
            ]
        }
    ]
}
