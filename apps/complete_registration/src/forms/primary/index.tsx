import { form } from "./primary.form"
import { InvoiceDetailsFormPage } from "./invoice_details.page"
import { PackageSelectFormPage } from "./package_select.page"
import { GeneralFormPage } from "./general.page"
export default {
    form,
    pages: [
        {
            id: "packages",
            page: PackageSelectFormPage
        },
        {
            id: "invoice_details",
            page: InvoiceDetailsFormPage
        },
        {
            id: "general",
            page: GeneralFormPage
        }
    ]
}
