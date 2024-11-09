import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card"
import { FORMS } from "@/forms"
import { AccessDeclarationArgs } from "@/forms/access_declaration_logic"
import { isFormOpen, isFormVisible } from "@/forms/form_access"
import { ContactBubble } from "@/screens/dashboard/ContactBubble"
import { getTimelinePhaseMessage } from "@/screens/dashboard/timeline_steps"
import { LogoutButton } from "@/shared/LogoutButton"
import { Timeline } from "@/shared/Timeline"
import { useAccessDeclaration } from "@/shared/hooks/api/useAccessDeclaration"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useDates } from "@/shared/hooks/api/useDates"
import { cx } from "@/utils/cx"
import LoadingAnimation from "@/utils/loading_animation/loading_animation"
import clsx from "clsx"
import { AlertTriangle, BadgeInfo, CheckCircle } from "lucide-react"
import { DateTime } from "luxon"
import { DashboardError } from "./DashboardError"
import FormCard from "./FormCard"

export function DashboardScreen({
    forceAccessDeclaration,
    hideContactBubble,
    hideName,
    hideLogout
}: {
    forceAccessDeclaration?: AccessDeclarationArgs
    hideContactBubble?: boolean
    hideName?: boolean
    hideLogout?: boolean
}) {
    const {
        data: dates,
        isLoading: isLoadingDates,
        isError: isErrorDates
    } = useDates()
    const { data, isLoading, isError } = useDashboard()
    const forms = FORMS

    const _accessDeclaration = useAccessDeclaration()
    const accessDeclaration = forceAccessDeclaration ?? _accessDeclaration

    const companyContact = data?.sales_contacts?.[0]

    if (isLoading || isLoadingDates) {
        return <LoadingAnimation />
    }

    // Check if root error
    if (isError || isErrorDates || data == null || dates == null) {
        return <DashboardError />
    }

    const formCardsData = Object.entries(forms).filter(([, formMeta]) =>
        isFormVisible(accessDeclaration, formMeta.key as keyof typeof FORMS)
    )

    const timelinePhaseAlert = getTimelinePhaseMessage(accessDeclaration)

    return (
        <div
            className={clsx("flex flex-col", {
                "min-h-[100dvh]": !hideContactBubble
            })}
        >
            {!hideLogout && (
                <div className="flex w-full justify-end">
                    <LogoutButton />
                </div>
            )}
            <div className={cx("flex flex-col-reverse md:flex-row")}>
                <div className="flex flex-1 flex-col items-center px-5">
                    <div className="flex flex-col items-center">
                        {!hideName && data.contact?.first_name != null && (
                            <Card className="max-w-[700px]">
                                <CardHeader>
                                    <CardTitle title={data.company.name}>
                                        Welcome <b>{data.contact.first_name}</b>
                                        !
                                    </CardTitle>
                                    <CardDescription>
                                        From this dashboard you will be able to
                                        configure your Armada experience. You
                                        will be able to provide information, buy
                                        products and read about our procedures
                                    </CardDescription>
                                </CardHeader>
                            </Card>
                        )}
                        {timelinePhaseAlert != null && (
                            <Alert className="mt-5 max-w-[700px]">
                                {timelinePhaseAlert.icon ??
                                    (timelinePhaseAlert.variant == null ||
                                    timelinePhaseAlert.variant === "info" ? (
                                        <BadgeInfo />
                                    ) : timelinePhaseAlert.variant ===
                                      "success" ? (
                                        <CheckCircle className="stroke-emerald-400" />
                                    ) : (
                                        <AlertTriangle className="stroke-yellow-400" />
                                    ))}
                                <AlertTitle className="ml-3">
                                    <span className="font-bold">
                                        {timelinePhaseAlert?.title ?? (
                                            <span>
                                                Current step:{" unknown"}
                                            </span>
                                        )}
                                    </span>
                                </AlertTitle>
                                <AlertDescription className="ml-3">
                                    {timelinePhaseAlert?.description}
                                </AlertDescription>
                            </Alert>
                        )}
                        <div className="mt-10 grid w-full grid-cols-1 gap-5 sm:grid-cols-2 2xl:grid-cols-3">
                            {formCardsData.map(([key, formMeta]) => (
                                <FormCard
                                    key={key}
                                    form={formMeta}
                                    locked={
                                        !isFormOpen(
                                            accessDeclaration,
                                            formMeta.key as keyof typeof FORMS
                                        )
                                    }
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </div>
            {!hideContactBubble && (
                <div className="relative flex flex-1 items-end justify-center">
                    <Timeline
                        className="mb-10 mt-20 h-28 w-2/3"
                        stages={[
                            {
                                when: [
                                    "initial_registration:::*:::*",
                                    "*:::signed_ir:::*",
                                    "*:::signed_cr:::*"
                                ],
                                title: "Initial Registration",
                                badgeText: `${DateTime.fromISO(
                                    dates.ir.start
                                ).toFormat("MMM d")} - ${DateTime.fromISO(
                                    dates.ir.end
                                ).toFormat("MMM d")}`
                            },
                            {
                                when: [
                                    "*:::signed_ir:::*",
                                    "*:::signed_cr:::*"
                                ],
                                title: "You have completed initial registration"
                            },
                            {
                                when: [
                                    "*:::signed_cr:::*",
                                    "complete_registration:::*:::*"
                                ],
                                title: "Final registration",
                                badgeText: `${DateTime.fromISO(
                                    dates.fr.start
                                ).toFormat("MMM d")} - ${DateTime.fromISO(
                                    dates.fr.end
                                ).toFormat("MMM d")}`
                            },
                            {
                                when: ["*:::signed_cr:::*"],
                                title: "You have completed final registration"
                            },
                            {
                                when: ["fair:::*:::*"],
                                title: "The fair 🥳",
                                badgeText: DateTime.fromISO(
                                    dates.fair.days.reduce(
                                        (acc, curr) =>
                                            DateTime.fromISO(acc) <
                                            DateTime.fromISO(curr)
                                                ? acc
                                                : curr,
                                        dates.fair.days[0]
                                    )
                                ).toFormat("MMM d")
                            }
                        ]}
                    />
                    {companyContact != null && (
                        <div className="absolute flex w-full justify-end p-4 lg:p-8">
                            <ContactBubble />
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
