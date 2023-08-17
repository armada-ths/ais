import { Form } from "../form_types"
import { InvoiceDetailsFormPage } from "../primary/invoice_details.page"
import { OrderDetails } from "./order_details.page"

export const form: Form = {
    key: "receipt",
    name: "Order & Invoice Details",
    description:
        "On this page you select products and entry of company invoice details. Once submitted, no changes are permitted.",
    forceFormDone: true,
    pages: [
        {
            id: "details",
            title: "Order details",
            hasNextButton: false,
            hasPrevButton: false,
            getProgress() {
                return 100
            },
            pageComponent: OrderDetails
        },
        {
            id: "invoice",
            title: "Invoice Information",
            hasNextButton: false,
            hasPrevButton: false,
            getProgress() {
                return 100
            },
            pageComponent: () => <InvoiceDetailsFormPage readOnly={true} />
        }
    ]
}
