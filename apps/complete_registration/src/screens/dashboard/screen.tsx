import { useSelector } from "react-redux"
import { cx } from "../../utils/cx"
import FormCard from "./FormCard"
import { selectForms } from "../../store/form/form_selectors"
import {
    selectCompanyStatus,
    selectUser
} from "../../store/company/company_selectors"
import { RegistrationStatus } from "../../store/company/company_slice"
import { FORMS } from "../../forms"
import { Card } from "../form/sidebar/PageCard"

export function DashboardScreen() {
    const forms = useSelector(selectForms)
    const companyStatus = useSelector(selectCompanyStatus)

    const FORM_CLOSED_DURING: Record<keyof typeof FORMS, RegistrationStatus[]> =
        {
            primary: ["complete_registration_signed"],
            lunch_tickets: [],
            exhibitor_catalog: [],
            transport: [],
            banquet_tickets: []
        }

    const user = useSelector(selectUser)

    return (
        <div className={cx("grid min-h-[100dvh] grid-cols-[1fr_6fr_1fr]")}>
            <div>{/* SIDEBAR */}</div>
            <div className="flex flex-col items-center p-5">
                <div className="flex max-w-6xl flex-col items-center">
                    <div>
                        <h1 className="rounded p-2 px-8 text-4xl text-emerald-400">
                            Company AB
                        </h1>
                    </div>
                    {user?.first_name != null && (
                        <Card className="col-span-full mt-10 max-w-xl border-0 bg-transparent bg-white p-5 text-gray-400">
                            <h2 className="mb-2 text-2xl">
                                Welcome <b>{user.first_name}</b>!
                            </h2>
                            <p className="text-sm">
                                From this dashboard you will be able to
                                configure your Armada experience. You will be
                                able to provide information, by products and
                                read about our procedures
                            </p>
                        </Card>
                    )}
                    <div className="mt-10 grid grid-cols-1 gap-5 lg:grid-cols-2 xl:grid-cols-3">
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
            </div>
            <div>{/* SIDEBAR */}</div>
        </div>
    )
}
