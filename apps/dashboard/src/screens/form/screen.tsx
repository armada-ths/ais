import { FORMS } from "@/forms"
import { isFormOpen } from "@/forms/form_access"
import { InfoScreen } from "@/shared/InfoScreen"
import { Navbar } from "@/shared/Navbar"
import { useDashboard } from "@/shared/hooks/useDashboard"
import { useFormMeta } from "@/useFormMeta"
import { cx } from "@/utils/cx"
import { FormPageView } from "./FormPageView"
import PrimarySection from "./PrimarySection"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"

export function FormScreen() {
    const { data: dashboardData } = useDashboard()

    const {
        form,
        formPage,
        formPageIndex,
        params: { formKey }
    } = useFormMeta()

    const companyStatus = dashboardData?.type

    const SideBar = form?.rightSidebar

    const formOpen = isFormOpen(
        formKey as keyof typeof FORMS,
        companyStatus ?? null
    )

    if (
        (form != null && formPage == null && formOpen) ||
        companyStatus == null
    ) {
        return null // We are still waiting for activeForm to be applied, hence show nothing to reduce flickering
    }
    if (form != null && formPage == null && !formOpen) {
        return (
            <InfoScreen
                severity="error"
                title="Access Denied"
                subText="The form you are trying to access is not available for your company. If you think this is a mistake, please contact sales at sales@armada.nu."
            />
        )
    }
    if (form == null || formPage == null) {
        return (
            <InfoScreen
                title="Oups, no form"
                subText="We could not find the form you were looking form"
            />
        )
    }

    return (
        <div>
            <Navbar />
            <div
                className={cx("grid min-h-[92vh] grid-cols-[1fr_3fr_1fr]", {
                    "grid-cols-[0_1fr_0]": !SideBar && form.pages.length <= 1
                })}
            >
                {form.pages.length > 1 ? (
                    // Only show the progression summary if there are multiple pages
                    <FormSidebarProgressionSummary />
                ) : (
                    <div className="" />
                )}
                <PrimarySection>
                    <FormPageView
                        form={form}
                        page={formPage}
                        pageIndex={formPageIndex}
                    />
                </PrimarySection>
                {SideBar != null && <SideBar />}
            </div>
        </div>
    )
}
