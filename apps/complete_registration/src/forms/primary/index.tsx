import { form } from "./primary.form"
import { InvoiceDetailsFormPage } from "./invoice_details.page"
import { PackageSelectFormPage } from "./package_select.page"
import { EventsFormPage } from "./events.page"
import { ExtrasFormPage } from "./extras.page"
import { SummaryFormPage } from "./summary.page"
export default {
    form,
    pages: [
        {
            id: "packages",
            page: PackageSelectFormPage
        },
        {
            id: "events",
            page: EventsFormPage
        },
        {
            id: "extras",
            page: ExtrasFormPage
        },
        {
            id: "invoice_details",
            page: InvoiceDetailsFormPage
        },
        {
            id: "summary",
            page: SummaryFormPage
        }
    ]
}
