import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import {
    Card,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card"
import { isFormOpen, isFormVisible } from "@/forms/form_access"
import { ContactBubble } from "@/screens/dashboard/ContactBubble"
import { getTimelinePhaseMessage } from "@/screens/dashboard/timeline_steps"
import { LogoutButton } from "@/shared/LogoutButton"
import { Timeline } from "@/shared/Timeline"
import { useRegistration } from "@/shared/hooks/useRegistration"
import { selectForms } from "@/store/form/form_selectors"
import { cx } from "@/utils/cx"
import LoadingAnimation from "@/utils/loading_animation/loading_animation"
import { BadgeInfo } from "lucide-react"
import { useSelector } from "react-redux"
import { DashboardError } from "./DashboardError"
import FormCard from "./FormCard"

export function DashboardScreen() {
    const { data, isLoading, isError } = useRegistration()
    const forms = useSelector(selectForms)

    const companyContact = data?.sales_contacts?.[0]

    /*     const colorClassName = {
        "text-red-400": companyProgress < 0.5,
        "text-yellow-400": companyProgress < 0.8,
        "text-emerald-400": companyProgress <= 1
    } */

    if (isLoading) {
        return <LoadingAnimation />
    }

    // Check if root error
    if (isError || data == null) {
        return <DashboardError />
    }

    const formCardsData = Object.entries(forms).filter(([, formMeta]) =>
        isFormVisible(formMeta.key, data.type ?? null)
    )

    return (
        <div className="flex min-h-[100dvh] flex-col">
            <div className={cx("grid grid-cols-[1fr_6fr_1fr]")}>
                <div>{/* SIDEBAR */}</div>
                <div className="flex flex-col items-center p-5">
                    <div className="mt-10 flex max-w-6xl flex-col items-center">
                        {data.contact?.first_name != null && (
                            <Card className="max-w-[700px]">
                                <CardHeader>
                                    <CardTitle>
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
                        {getTimelinePhaseMessage(data.type) != null && (
                            <Alert className="mt-5 max-w-[700px]">
                                <BadgeInfo />
                                <AlertTitle className="ml-3">
                                    <span className="font-bold">
                                        {getTimelinePhaseMessage(data.type)
                                            ?.title ?? (
                                            <span>
                                                Current step:{" "}
                                                {data.type.split("_").join(" ")}
                                            </span>
                                        )}
                                    </span>
                                </AlertTitle>
                                <AlertDescription className="ml-3">
                                    {
                                        getTimelinePhaseMessage(data.type)
                                            ?.description
                                    }
                                </AlertDescription>
                            </Alert>
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
                                            data.type ?? null
                                        )
                                    }
                                />
                            ))}
                        </div>
                    </div>
                </div>
                <div className="flex flex-col items-center">
                    <LogoutButton />
                </div>
            </div>
            <div className="relative flex flex-1 items-end justify-center">
                <Timeline
                    className="mb-10 h-28 w-2/3"
                    stages={[
                        {
                            id: [
                                "initial_registration",
                                "after_initial_registration"
                            ],
                            title: "Initial Registration"
                        },
                        {
                            id: [
                                "after_initial_registration_signed",
                                "initial_registration_signed"
                            ],
                            title: "You have completed initial registration"
                        },
                        {
                            id: [
                                /*                                     "complete_registration_ir_unsigned", */
                            ],
                            title: "You got a spot at the fair"
                        },
                        {
                            id: [
                                "complete_registration_ir_signed",
                                "complete_registration_ir_unsigned",
                                "complete_registration_signed"
                            ],
                            title: "Final registration",
                            badgeText: "Aug 20"
                        },
                        {
                            id: [
                                "complete_registration_ir_signed",
                                "complete_registration_ir_unsigned",
                                "complete_registration_signed"
                            ],
                            title: "You have completed final registration"
                        },
                        {
                            id: [],
                            title: "The fair 🥳"
                        }
                    ]}
                    current={data.type}
                />
                {companyContact != null && (
                    <div className="absolute flex w-full justify-end p-4 lg:p-8">
                        <ContactBubble />
                    </div>
                )}
            </div>
        </div>
    )
}
