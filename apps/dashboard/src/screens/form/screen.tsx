import { useParams } from "@tanstack/react-router"
import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { FORMS } from "../../forms"
import { isFormOpen } from "../../forms/form_access"
import { InfoScreen } from "../../shared/InfoScreen"
import { Navbar } from "../../shared/Navbar"
import { selectCompanyStatus } from "../../store/company/company_selectors"
import {
    selectActivePage,
    selectActivePageIndex,
    selectForm
} from "../../store/form/form_selectors"
import { setActiveForm } from "../../store/form/form_slice"
import { RootState } from "../../store/store"
import { cx } from "../../utils/cx"
import { FormPageView } from "./FormPageView"
import PrimarySection from "./PrimarySection"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"

export function FormScreen() {
    const dispatch = useDispatch()
    const { formKey } = useParams()

    const activePage = useSelector(selectActivePage)
    const activePageIndex = useSelector(selectActivePageIndex)
    const form = useSelector((state: RootState) =>
        selectForm(state, formKey as keyof typeof FORMS)
    )
    const companyStatus = useSelector(selectCompanyStatus)

    const SideBar = form?.rightSidebar

    const formOpen = isFormOpen(
        formKey as keyof typeof FORMS,
        companyStatus ?? null
    )

    useEffect(() => {
        if (
            formKey != null &&
            FORMS[formKey as keyof typeof FORMS] != null && // Form exists
            isFormOpen(formKey as keyof typeof FORMS, companyStatus ?? null) // Form is open
        ) {
            dispatch(setActiveForm(formKey as keyof typeof FORMS))
        }
    }, [formKey, form, dispatch, companyStatus])

    if (
        (form != null && activePage == null && formOpen) ||
        companyStatus == null
    ) {
        return null // We are still waiting for activeForm to be applied, hence show nothing to reduce flickering
    }
    if (form != null && activePage == null && !formOpen) {
        return (
            <InfoScreen
                severity="error"
                title="Access Denied"
                subText="The form you are trying to access is not available for your company. If you think this is a mistake, please contact sales at sales@armada.nu."
            />
        )
    }
    if (form == null || activePage == null) {
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
                        page={activePage}
                        pageIndex={activePageIndex}
                    />
                </PrimarySection>
                {SideBar != null && <SideBar />}
            </div>
        </div>
    )
}
