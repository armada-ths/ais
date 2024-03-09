import { Form } from "../form_types"
import { InvoiceDetailsFormPage } from "../primary/invoice_details.page"
import { OrderDetails } from "./order_details.page"

export const form = {
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
            isDone: null,
            pageComponent: OrderDetails
        },
        {
            id: "invoice",
            title: "Invoice Information",
            hasNextButton: false,
            hasPrevButton: false,
            isDone: null,
            pageComponent: () => (
                <div>
                    <div className="flex w-full justify-center">
                        <div className="mb-2 w-[450px] rounded bg-slate-200 p-2 px-4">
                            <p className="text-slate-600">
                                If you want to change invoice details, please
                                contact your sales representatives.
                            </p>
                        </div>
                    </div>
                    <InvoiceDetailsFormPage readOnly={true} />
                </div>
            )
        }
    ]
} as const satisfies Form
