import {
    AccessDeclaration,
    AccessDeclarationArgs,
    parseAccessDeclaration
} from "@/forms/access_declaration_logic"

export const TIMELINE_STEPS: Partial<
    Record<
        AccessDeclaration,
        {
            title?: React.ReactNode
            description: React.ReactNode
            variant?: "info" | "success" | "warning" // Default info
        }
    >
> = {
    "before_initial_registration:::*:::*": {
        title: "This year's fair is still under development",
        description:
            "We're still working on the initial registration, come back later..."
    },
    "initial_registration:::*:::*": {
        title: "Welcome to Armada!",
        description:
            "To get a spot in this year's event, please complete the initial registration"
    },
    "initial_registration:::ir_signed:::*": {
        title: "You have completed this year's initial registration",
        description:
            "We'll be in touch! Feel free to add additional information about your company",
        variant: "success"
    },
    "between_ir_and_cr:::*:::*": {
        title: "You have completed this year's initial registration",
        description: "We'll be in touch!",
        variant: "success"
    },
    "between_ir_and_cr:::unsigned:::*": {
        title: "You did not complete the initial registration",
        description: (
            <>
                All hope is not lost! Please contact our sales team:{" "}
                <a href="mailto:sales@armada.nu" className="underline">
                    sales@armada.nu
                </a>
            </>
        ),
        variant: "warning"
    },
    "between_ir_and_cr:::*:::accepted": {
        title: "Congratulations! You've got a spot at the fair",
        description: "We'll be in touch with more information",
        variant: "success"
    },
    "between_ir_and_cr:::*:::rejected": {
        title: "We are at full capacity",
        description:
            "Unfortunately, we are unable to offer you a spot at the fair, if any spot appears we will contact you",
        variant: "warning"
    },
    "between_ir_and_cr:::*:::pending": {
        title: "Welcome!",
        description: (
            <>
                We are currently processing your application. If you have any
                questions contact us at
                <a href="mailto:sales@armada.nu" className="underline">
                    sales@armada.nu
                </a>{" "}
            </>
        ),
        variant: "info"
    },
    "complete_registration:::cr_signed:::*": {
        title: "You have completed the final registration",
        description:
            "Please make sure to fill in the remaining cards. See you at the fair!",
        variant: "success"
    },
    "complete_registration:::ir_signed:::*": {
        title: "Welcome to the Armada final registration!",
        description:
            "Complete the registration to participate in this year's event"
    },
    "complete_registration:::unsigned:::*": {
        title: "Welcome to the Armada final registration!",
        description:
            "You have not completed the initial registration, please contact our sales team",
        variant: "warning"
    }
}

export function getTimelinePhaseMessage(state: AccessDeclarationArgs | null) {
    return parseAccessDeclaration(state, TIMELINE_STEPS)?.value
}
