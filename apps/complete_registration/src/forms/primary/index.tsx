import { form } from "./primary.form"
import { InvoiceDetailsFormPage } from "./invoice_details.page"
import { PackageSelectFormPage } from "./package_select.page"
import { ProductFormPage } from "./product.page"
import { SummaryFormPage } from "./summary.page"
import {
    selectProductEvents,
    selectProductExtras
} from "../../store/products/products_selectors"
export default {
    form,
    pages: [
        {
            id: "packages",
            page: PackageSelectFormPage
        },
        {
            id: "events",
            page: () => <ProductFormPage selector={selectProductEvents} />
        },
        {
            id: "extras",
            page: () => <ProductFormPage selector={selectProductExtras} />
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
