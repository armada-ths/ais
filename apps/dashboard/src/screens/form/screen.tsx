import PrimarySection from "./PrimarySection"
import { FormPageView } from "./FormPageView"
import { useDispatch, useSelector } from "react-redux"
import {
    selectActivePage,
    selectActivePageIndex,
    selectForm
} from "../../store/form/form_selectors"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"
import { cx } from "../../utils/cx"
import { Navbar } from "../../shared/Navbar"
import { InfoScreen } from "../../shared/InfoScreen"
import { useParams } from "@tanstack/react-router"
import { FORMS } from "../../forms"
import { useEffect } from "react"
import { setActiveForm } from "../../store/form/form_slice"
import { isFormOpen } from "../../forms/form_access"
import { selectCompanyStatus } from "../../store/company/company_selectors"
import { RootState } from "../../store/store"

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
            <div className={cx("grid min-h-[92vh] grid-cols-[1fr_3fr_1fr]")}>
                <FormSidebarProgressionSummary />
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
