import { RegistrationStatus } from "@/store/company/company_slice"

export const TIMELINE_STEPS: Partial<
    Record<
        RegistrationStatus,
        {
            title?: string
            description: string
        }
    >
> = {
    before_initial_registration: {
        title: "This year's fair is still under development",
        description:
            "We haven't finalized this year's contract yet, come back later..."
    },
    initial_registration: {
        title: "Welcome to Armada!",
        description:
            "To participate in this year's event, please complete the initial registration"
    },
    initial_registration_signed: {
        title: "You have signed this year's contract",
        description: "We'll be in touch!"
    },
    after_initial_registration: {
        title: "You did not complete the initial registration",
        description: "All hope is not lost! Please contact our sales team"
    },
    after_initial_registration_signed: {
        title: "You have signed this year's contract",
        description: "We'll be in touch!"
    },
    before_complete_registration: {
        title: "",
        description: ""
    }
}

export function getTimelinePhaseMessage(status: RegistrationStatus) {
    return TIMELINE_STEPS[status]
}
