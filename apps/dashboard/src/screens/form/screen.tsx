import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FORMS, FormIds, FormPageIds } from "@/forms"
import { isFormOpen } from "@/forms/form_access"
import { IfProgressDone } from "@/shared/IfProgressDone"
import { InfoScreen } from "@/shared/InfoScreen"
import { Navbar } from "@/shared/Navbar"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { remoteSaveChanges } from "@/store/form/async_actions"
import { AppDispatch } from "@/store/store"
import { useFormMeta } from "@/useFormMeta"
import { cx } from "@/utils/cx"
import { useNavigate } from "@tanstack/react-router"
import { ArrowLeft, ArrowRight, CheckCircle } from "lucide-react"
import { useDispatch } from "react-redux"
import { FormPageView } from "./FormPageView"
import PrimarySection from "./PrimarySection"
import { FormSidebarProgressionSummary } from "./sidebar/FormSidebarProgressionSummary"

export function FormScreen() {
    const dispatch = useDispatch<AppDispatch>()
    const navigate = useNavigate({
        from: "/$companyId/form/$formKey/$formPageKey"
    })
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

    async function saveChanges() {
        const response = await dispatch(remoteSaveChanges())
        return (response.payload as { success: boolean }).success
    }

    async function handlePrevious() {
        if (!form) return
        const previousPage = form.pages[formPageIndex - 1]
        navigate({
            to: "/$companyId/form/$formKey/$formPageKey",
            params: { formPageKey: previousPage.id }
        })
    }

    async function handleNext() {
        if (!form) return
        const nextPage = form.pages[formPageIndex + 1]
        navigate({
            from: "/$companyId/form/$formKey/$formPageKey",
            to: "/$companyId/form/$formKey/$formPageKey",
            params: { formPageKey: nextPage.id }
        })
    }

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

    const PrevButton = ({
        variant,
        disabled
    }: {
        variant?: "secondary" | "outline"
        disabled?: boolean
    }) => (
        <Button
            disabled={disabled}
            variant={variant ?? "secondary"}
            onClick={handlePrevious}
            className={cx({
                "!opacity-0": disabled
            })}
        >
            <ArrowLeft className="pr-2" size={25} />
            Previous
        </Button>
    )

    const NextButton = ({
        variant,
        disabled
    }: {
        variant?: "secondary" | "outline"
        disabled?: boolean
    }) => (
        <Button
            disabled={disabled}
            variant={variant ?? "secondary"}
            onClick={handleNext}
            className={cx("", {
                "!opacity-0": disabled
            })}
        >
            Next
            <ArrowRight className="pl-2" size={25} />
        </Button>
    )

    return (
        <div>
            <Navbar
                titleLeft={
                    <PrevButton
                        variant="outline"
                        disabled={
                            !(
                                formPageIndex > 0 &&
                                formPage.hasPrevButton !== false
                            )
                        }
                    />
                }
                titleRight={
                    <NextButton
                        variant="outline"
                        disabled={formPage.hasNextButton === false}
                    />
                }
            />
            <Tabs value={formPage.id} className="lg:hidden">
                <div className="flex w-full justify-center py-2">
                    <TabsList>
                        {form.pages.map(page => (
                            <TabsTrigger
                                key={page.id}
                                id={page.id} // Important to allow the tab to be clickable (see above comment)
                                value={page.id}
                                onClick={async () => {
                                    await saveChanges()
                                    navigate({
                                        from: "/$companyId/form/$formKey/$formPageKey",
                                        to: "/$companyId/form/$formKey/$formPageKey",
                                        params: {
                                            formPageKey: page.id
                                        }
                                    })
                                }}
                            >
                                <IfProgressDone
                                    page={
                                        `${form.key}.${page.id}` as `${FormIds}.${FormPageIds}`
                                    }
                                >
                                    <CheckCircle
                                        size={20}
                                        className="stroke-melon-700 pr-2"
                                    />
                                </IfProgressDone>
                                {page.title}
                            </TabsTrigger>
                        ))}
                    </TabsList>
                </div>
                {form.pages.map(page => (
                    <TabsContent key={page.id} value={page.id}>
                        <PrimarySection>
                            <FormPageView
                                formId={form.key as keyof typeof FORMS}
                                page={page}
                            />
                        </PrimarySection>
                    </TabsContent>
                ))}
            </Tabs>
            <div
                className={cx(
                    "hidden min-h-[92vh] grid-cols-[1fr_3fr_1fr] lg:grid",
                    {
                        "grid-cols-[0_1fr_0]":
                            !SideBar && form.pages.length <= 1
                    }
                )}
            >
                {form.pages.length > 1 ? (
                    // Only show the progression summary if there are multiple pages
                    <FormSidebarProgressionSummary />
                ) : (
                    <div className="" />
                )}
                <PrimarySection>
                    <FormPageView
                        formId={form.key as keyof typeof FORMS}
                        page={formPage}
                    />
                </PrimarySection>
                {SideBar != null && <SideBar />}
            </div>
        </div>
    )
}
