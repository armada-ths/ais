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

const states: AccessDeclarationArgs[] = Object.values(
    RegistrationPeriod
).flatMap(period =>
    Object.values(ApplicationStatus).flatMap(applicationStatus =>
        Object.values(SigningStep).map(signingStep => ({
            period,
            applicationStatus,
            signingStep
        }))
    )
)

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
