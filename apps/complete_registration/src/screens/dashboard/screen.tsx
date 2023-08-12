import { useSelector } from "react-redux"
import { cx } from "../../utils/cx"
import FormCard from "./FormCard"
import {
    selectCompanyProgress,
    selectForms
} from "../../store/form/form_selectors"
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
    const companyProgress = useSelector(selectCompanyProgress)

    const FORM_CLOSED_DURING: Record<keyof typeof FORMS, RegistrationStatus[]> =
        {
            primary: ["complete_registration_signed"],
            lunch_tickets: [],
            exhibitor_catalog: [],
            transport: [],
            banquet_tickets: []
        }

    const user = useSelector(selectUser)

    const colorClassName = {
        "text-red-400": companyProgress < 0.5,
        "text-yellow-400": companyProgress < 0.8,
        "text-emerald-400": companyProgress <= 1
    }

    if (user == null) {
        return (
            <div className="flex h-[100vh] w-[100vw] items-center justify-center">
                <p>
                    You are not logged in, you can{" "}
                    <a className="text-emerald-400 underline" href="/register">
                        sign in here
                    </a>
                </p>
            </div>
        )
    }

    return (
        <div className={cx("grid min-h-[100dvh] grid-cols-[1fr_6fr_1fr]")}>
            <div>{/* SIDEBAR */}</div>
            <div className="flex flex-col items-center p-5">
                <div className="flex max-w-6xl flex-col items-center">
                    <div className="grid w-full grid-cols-[1fr_2fr_1fr]">
                        <div />
                        <h1 className="rounded p-2 px-8 text-center text-4xl text-emerald-400">
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
                    <div className="mt-10 flex flex-col items-center justify-end">
                        <p className={cx("mb-2 text-xl", colorClassName)}>
                            {companyProgress < 1
                                ? "Company Progress"
                                : "Fully Configured"}
                        </p>
                        <p className={cx("text-4xl font-bold", colorClassName)}>
                            {companyProgress < 1 ? (
                                `${(companyProgress * 100).toFixed()}%`
                            ) : (
                                <span className="pi pi-check-circle !text-4xl !font-bold" />
                            )}
                        </p>
                    </div>
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
