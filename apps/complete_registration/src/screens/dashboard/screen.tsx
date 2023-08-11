import { useSelector } from "react-redux"
import { cx } from "../../utils/cx"
import FormCard from "./FormCard"
import { selectForms } from "../../store/form/form_selectors"
import { selectCompanyStatus } from "../../store/company/company_selectors"
import { RegistrationStatus } from "../../store/company/company_slice"
import { FORMS } from "../../forms"

export function DashboardScreen() {
    const forms = useSelector(selectForms)
    const companyStatus = useSelector(selectCompanyStatus)

    const FORM_CLOSED_DURING: Record<keyof typeof FORMS, RegistrationStatus[]> =
        {
            primary: ["complete_registration_signed"],
            create_lunch_tickets: [],
            exhibitor_catalog: [],
            transport: []
        }

    return (
        <div className={cx("grid min-h-[100dvh] grid-cols-[1fr_6fr_1fr]")}>
            <div>{/* SIDEBAR */}</div>
            <div className="flex flex-col items-center p-5">
                <div>
                    <h1 className="rounded bg-slate-400 p-2 px-8 text-4xl text-white">
                        Company AB
                    </h1>
                </div>
                <div className="mt-10 grid grid-cols-1 gap-5 xl:grid-cols-2 3xl:grid-cols-3">
                    {Object.entries(forms).map(([key, formMeta]) => (
                        <FormCard
                            key={key}
                            form={formMeta}
                            locked={
                                companyStatus != null &&
                                FORM_CLOSED_DURING[formMeta.key].includes(
                                    companyStatus
                                )
                            }
                        />
                    ))}
                </div>
            </div>
            <div>{/* SIDEBAR */}</div>
        </div>
    )
}
