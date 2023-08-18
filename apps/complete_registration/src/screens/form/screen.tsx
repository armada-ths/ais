import PrimarySection from "./PrimarySection"
import { FormPageView } from "./FormPageView"
import { useSelector } from "react-redux"
import {
    selectActiveForm,
    selectActivePage,
    selectActivePageIndex
} from "../../store/form/form_selectors"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"
import { cx } from "../../utils/cx"
import { Navbar } from "../../shared/Navbar"
import { InfoScreen } from "../../shared/InfoScreen"

export function FormScreen() {
    const activePage = useSelector(selectActivePage)
    const activePageIndex = useSelector(selectActivePageIndex)
    const activeForm = useSelector(selectActiveForm)

    if (activeForm == null || activePage == null) {
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
                        form={activeForm}
                        page={activePage}
                        pageIndex={activePageIndex}
                    />
                </PrimarySection>
                {activeForm.rightSidebar?.()}
            </div>
        </div>
    )
}
