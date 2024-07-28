import { RegistrationStatus } from "@/store/company/company_slice"

export const TIMELINE_STEPS: Partial<
    Record<
        RegistrationStatus,
        {
            title?: React.ReactNode
            description: React.ReactNode
            variant?: "info" | "success" | "warning" // Default info
        }
    >
> = {
    before_initial_registration: {
        title: "This year's fair is still under development",
        description:
            "We're still working on the initial registration, come back later..."
    },
    initial_registration: {
        title: "Welcome to Armada!",
        description:
            "To get a spot in this year's event, please complete the initial registration"
    },
    initial_registration_signed: {
        title: "You have completed this year's initial registration",
        description:
            "We'll be in touch! Feel free to add additional information about your company",
        variant: "success"
    },
    after_initial_registration: {
        title: "You did not complete the initial registration",
        description:
            <>All hope is not lost! Please contact our sales team: <a href="mailto:sales@armada.nu" className="underline">sales@armada.nu</a></>,
        variant: "warning"
    },
    after_initial_registration_signed: {
        title: "You have completed this year's initial registration",
        description: "We'll be in touch!",
        variant: "success"
    },
    after_initial_registration_acceptance_accepted: {
        title: "Congratulations! You've got a spot at the fair",
        description: "We'll be in touch with more information",
        variant: "success"
    },
    after_initial_registration_acceptance_rejected: {
        title: "We are at full capacity",
        description:
            "Unfortunately, we are unable to offer you a spot at the fair, if any spot appears we will contact you",
        variant: "warning"
    },
    after_initial_registration_acceptance_tentative: {
        title: "Welcome!",
        description: (
            <>Please contact our sales team <a href="mailto:sales@armada.nu" className="underline">sales@armada.nu</a> for a spot on the fair.</>
        ),
        variant: "info"
    },
    complete_registration_ir_signed: {
        title: "Welcome to the Armada final registration!",
        description:
            "Complete the registration to participate in this year's event"
    },
    complete_registration_ir_unsigned: {
        title: "Welcome to the Armada final registration!",
        description:
            "You have not completed the initial registration, please contact our sales team",
        variant: "warning"
    },
    complete_registration_signed: {
        title: "You have completed the final registration",
        description:
            "Please make sure to fill in the remaining cards. See you at the fair!",
        variant: "success"
    }
}

export function getTimelinePhaseMessage(status: RegistrationStatus) {
    return TIMELINE_STEPS[status]
}
