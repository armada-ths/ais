import { useSelector } from "react-redux"
import { cx } from "../../utils/cx"
import FormCard from "./FormCard"
import { selectErrors, selectForms } from "../../store/form/form_selectors"
import {
    selectCompanyName,
    selectCompanyStatus,
    selectUser
} from "../../store/company/company_selectors"
import { Card } from "../form/sidebar/PageCard"
import { DashboardError } from "./DashboardError"
import { LogoutButton } from "../../shared/LogoutButton"
import { isFormHidden, isFormOpen } from "../../forms/form_access"

export function DashboardScreen() {
    const forms = useSelector(selectForms)
    const companyStatus = useSelector(selectCompanyStatus)
    /*     const companyProgress = useSelector(selectCompanyProgress) */
    const selectError = useSelector(selectErrors)
    const companyName = useSelector(selectCompanyName)
    const user = useSelector(selectUser)

    /*     const colorClassName = {
        "text-red-400": companyProgress < 0.5,
        "text-yellow-400": companyProgress < 0.8,
        "text-emerald-400": companyProgress <= 1
    } */

    // Check if root error
    if (selectError != null && typeof selectError === "string") {
        return <DashboardError />
    }

    const formCardsData = Object.entries(forms).filter(
        ([, formMeta]) =>
            isFormHidden(formMeta.key, companyStatus ?? null) === false
    )

    return (
        <div className={cx("grid min-h-[100dvh] grid-cols-[1fr_6fr_1fr]")}>
            <div>{/* SIDEBAR */}</div>
            <div className="flex flex-col items-center p-5">
                <div className="flex max-w-6xl flex-col items-center">
                    <div className="grid w-full grid-cols-[1fr_2fr_1fr]">
                        <div />
                        <h1 className="rounded p-2 px-8 text-center text-4xl text-emerald-400">
                            {companyName}
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
                    {/*                     <div className="mt-10 flex flex-col items-center justify-end">
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
                    </div> */}
                    <div className="mt-10 grid grid-cols-1 gap-5 lg:grid-cols-2 xl:grid-cols-3">
                        {formCardsData.map(([key, formMeta]) => (
                            <FormCard
                                key={key}
                                form={formMeta}
                                locked={
                                    !isFormOpen(
                                        formMeta.key,
                                        companyStatus ?? null
                                    )
                                }
                            />
                        ))}
                    </div>
                </div>
            </div>
            <div className="flex flex-col items-center">
                <LogoutButton />
                <div className="flex-1" />
            </div>
        </div>
    )
}
