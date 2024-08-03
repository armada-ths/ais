import { AccessDeclarationArgs } from "@/forms/access_declaration_logic"
import { DashboardScreen } from "@/screens/dashboard/screen"
import {
    ApplicationStatus,
    RegistrationPeriod
} from "@/shared/hooks/api/useDashboard"

const AllApplicationStatuses = [
    ApplicationStatus.UNSIGNED_IR,
    ApplicationStatus.PENDING,
    ApplicationStatus.ACCEPTED,
    ApplicationStatus.REJECTED,
    ApplicationStatus.WAITLIST
]

const Combinations: AccessDeclarationArgs[] = [
    {
        period: RegistrationPeriod.BeforeIr,
        exhibitorStatus: ApplicationStatus.UNSIGNED_IR
    },
    ...AllApplicationStatuses.map(exhibitorStatus => ({
        period: RegistrationPeriod.InitialRegistration,
        exhibitorStatus
    })),
    ...AllApplicationStatuses.map(exhibitorStatus => ({
        period: RegistrationPeriod.BetweenIrAndCr,
        exhibitorStatus
    })),
    ...[...AllApplicationStatuses, ApplicationStatus.SIGNED_CR].map(
        exhibitorStatus => ({
            period: RegistrationPeriod.CompleteRegistration,
            exhibitorStatus
        })
    ),
    ...[...AllApplicationStatuses, ApplicationStatus.SIGNED_CR].map(
        exhibitorStatus => ({
            period: RegistrationPeriod.AfterCompleteRegistration,
            exhibitorStatus
        })
    ),
    ...[...AllApplicationStatuses, ApplicationStatus.SIGNED_CR].map(
        exhibitorStatus => ({
            period: RegistrationPeriod.Fair,
            exhibitorStatus
        })
    ),
    ...[...AllApplicationStatuses, ApplicationStatus.SIGNED_CR].map(
        exhibitorStatus => ({
            period: RegistrationPeriod.AfterFair,
            exhibitorStatus
        })
    )
]

export function VisualizeScreen() {
    return (
        <>
            {Combinations.map((arg, i) => (
                <div className="m-5 border-2 border-black p-2 pb-10" key={i}>
                    <h1 className="pl-5 text-2xl">
                        {arg.period} - {arg.exhibitorStatus}
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
