import { Button } from "@/components/ui/button"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger
} from "@/components/ui/select"
import { AccessDeclarationArgs } from "@/forms/access_declaration_logic"
import { DashboardScreen } from "@/screens/dashboard/screen"
import {
    ApplicationStatus,
    RegistrationPeriod,
    SigningStep
} from "@/shared/hooks/api/useDashboard"
import { useMemo, useState } from "react"

function withPeriod(
    period: RegistrationPeriod,
    states: Pick<AccessDeclarationArgs, "applicationStatus" | "signingStep">[]
) {
    return states.map(({ applicationStatus, signingStep }) => ({
        period,
        applicationStatus,
        signingStep
    }))
}

function withSigned(
    signingStep: SigningStep,
    applicationStatuses: AccessDeclarationArgs["applicationStatus"][]
) {
    return applicationStatuses.map(applicationStatus => ({
        applicationStatus,
        signingStep
    }))
}

const states: AccessDeclarationArgs[] = [
    {
        period: RegistrationPeriod.BeforeIr,
        applicationStatus: ApplicationStatus.NONE,
        signingStep: SigningStep.UNSIGNED_IR
    },
    ...withPeriod(RegistrationPeriod.InitialRegistration, [
        {
            applicationStatus: ApplicationStatus.NONE,
            signingStep: SigningStep.UNSIGNED_IR
        },
        ...withSigned(SigningStep.SIGNED_IR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ])
    ]),
    ...withPeriod(RegistrationPeriod.BetweenIrAndCr, [
        {
            applicationStatus: ApplicationStatus.NONE,
            signingStep: SigningStep.UNSIGNED_IR
        },
        ...withSigned(SigningStep.SIGNED_IR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ])
    ]),
    ...withPeriod(RegistrationPeriod.CompleteRegistration, [
        {
            applicationStatus: ApplicationStatus.NONE,
            signingStep: SigningStep.UNSIGNED_IR
        },
        ...withSigned(SigningStep.SIGNED_IR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ]),
        ...withSigned(SigningStep.SIGNED_CR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ])
    ]),
    ...withPeriod(RegistrationPeriod.AfterCompleteRegistration, [
        {
            applicationStatus: ApplicationStatus.NONE,
            signingStep: SigningStep.UNSIGNED_IR
        },
        ...withSigned(SigningStep.SIGNED_IR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ]),
        ...withSigned(SigningStep.SIGNED_CR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ])
    ]),
    ...withPeriod(RegistrationPeriod.Fair, [
        {
            applicationStatus: ApplicationStatus.NONE,
            signingStep: SigningStep.UNSIGNED_IR
        },
        ...withSigned(SigningStep.SIGNED_IR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ]),
        ...withSigned(SigningStep.SIGNED_CR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ])
    ]),
    ...withPeriod(RegistrationPeriod.AfterFair, [
        {
            applicationStatus: ApplicationStatus.NONE,
            signingStep: SigningStep.UNSIGNED_IR
        },
        ...withSigned(SigningStep.SIGNED_IR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ]),
        ...withSigned(SigningStep.SIGNED_CR, [
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.REJECTED,
            ApplicationStatus.WAITLIST
        ])
    ])
]

export function VisualizeScreen() {
    const [registrationPeriod, setRegistrationPeriod] =
        useState<RegistrationPeriod>()
    const [signingState, setSigningState] = useState<SigningStep>()
    const [applicationStatus, setApplicationStatus] =
        useState<ApplicationStatus>()

    const visibleStates = useMemo(
        () =>
            states
                .filter(state => {
                    if (registrationPeriod == null) return true
                    return state.period === registrationPeriod
                })
                .filter(state => {
                    if (signingState == null) return true
                    return state.signingStep === signingState
                })
                .filter(state => {
                    if (applicationStatus == null) return true
                    return state.applicationStatus === applicationStatus
                }),
        [applicationStatus, registrationPeriod, signingState]
    )

    if (!import.meta.env.DEV) {
        return null
    }

    return (
        <>
            <div className="mx-auto flex max-w-2xl gap-2 p-4">
                <Select
                    value={registrationPeriod}
                    onValueChange={period =>
                        setRegistrationPeriod(period as RegistrationPeriod)
                    }
                >
                    <SelectTrigger>
                        {registrationPeriod ?? "Period"}
                    </SelectTrigger>
                    <SelectContent>
                        {Object.values(RegistrationPeriod).map(period => (
                            <SelectItem key={period} value={period}>
                                {period}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
                <Select
                    value={signingState}
                    onValueChange={signingStatus =>
                        setSigningState(signingStatus as SigningStep)
                    }
                >
                    <SelectTrigger>
                        {signingState ?? "Signing state"}
                    </SelectTrigger>
                    <SelectContent>
                        {Object.values(SigningStep).map(period => (
                            <SelectItem key={period} value={period}>
                                {period}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
                <Select
                    value={applicationStatus}
                    onValueChange={applicationStatus =>
                        setApplicationStatus(
                            applicationStatus as ApplicationStatus
                        )
                    }
                >
                    <SelectTrigger>
                        {applicationStatus ?? "Application status"}
                    </SelectTrigger>
                    <SelectContent>
                        {Object.values(ApplicationStatus).map(period => (
                            <SelectItem key={period} value={period}>
                                {period}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
                <Button
                    onClick={() => {
                        setRegistrationPeriod(undefined)
                        setSigningState(undefined)
                        setApplicationStatus(undefined)
                    }}
                >
                    Clear filters
                </Button>
            </div>
            {visibleStates.map(arg => (
                <div
                    className="m-5 border-2 border-black p-2 pb-10"
                    key={`${arg.applicationStatus}_${arg.period}_${arg.signingStep}`}
                >
                    <h1 className="pl-5 text-2xl">
                        {arg.period} - {arg.signingStep} -{" "}
                        {arg.applicationStatus}
                    </h1>
                    <DashboardScreen
                        hideContactBubble
                        hideName
                        hideLogout
                        forceAccessDeclaration={arg}
                    />
                </div>
            ))}
        </>
    )
}
