import {
    AccessDeclaration,
    AccessDeclarationArgs,
    parseAccessDeclaration
} from "@/forms/access_declaration_logic"
import { Hourglass } from "lucide-react"

type TimelineStep = {
    title?: React.ReactNode
    description: React.ReactNode
    variant?: "info" | "success" | "warning" // Default info
    icon?: React.ReactNode
}

const salesEmail = (
    <a href="mailto:sales@armada.nu" className="underline">
        sales@armada.nu
    </a>
)

const newSignupForm = <a href="">Armada 2025 sign up form</a>

export const TIMELINE_STEPS: Partial<Record<AccessDeclaration, TimelineStep>> =
    {
        "fair:::signed_cr:::!accepted": {
            title: "Welcome to Armada!",
            description: (
                <>
                    Unfortunately we could not offer you a spot at this year's
                    event. We're looking forward to seeing you at next year's
                    event, make an early sign up at {newSignupForm}
                </>
            )
        },
        "after_fair:::*:::!accepted": {
            title: "Welcome to Armada!",
            description: (
                <>
                    We're looking forward to seeing you at next year's event,
                    you can sign up here {newSignupForm}
                </>
            )
        },
        "*:::*:::rejected": {
            title: "We are at full capacity",
            description:
                "Unfortunately, we are unable to offer you a spot at the fair, if any spot appears we will contact you.",
            variant: "warning"
        },
        "before_initial_registration:::*:::*": {
            title: "This year's fair is still under development",
            description:
                "We're still working on this year's initial registration, please come back later!"
        },
        "complete_registration:::unsigned_ir:::*": {
            title: "Welcome to Armada!",
            description:
                "To request a spot at the fair, please first complete the below initial registration. You will then be able to complete the final registration."
        },
        "complete_registration:::!signed_cr:::accepted": {
            title: "You've got a spot in the fair!",
            description:
                "Please complete the below registration to finalize your spot at the fair."
        },
        "complete_registration:::!signed_cr:::waitlist": {
            title: "You have been placed in the waitlist!",
            description:
                "Please complete the below registration to finalize your request for a spot at the fair.",
            icon: <Hourglass className="stroke-emerald-400" />
        },
        "complete_registration:::!signed_cr:::*": {
            title: "Welcome to the Armada final registration!",
            description:
                "Please complete the below registration to finalize your request for a spot at the fair."
        },
        "complete_registration:::signed_cr:::pending": {
            title: "You have completed the final registration!",
            description:
                "We are currently processing your application. Meanwhile, please make sure to fill in the remaining cards.",
            variant: "success"
        },
        "complete_registration:::signed_cr:::accepted": {
            title: "You have completed the final registration!",
            description:
                "Your final registration is accepted! If you have any questions about your registration, contact sales@armada.nu. Otherwise, you can wait until the host assigned to you contacts you with more information closer to the fair. If you haven't filled in your company information in the dashboard yet, please do so.",
            variant: "success"
        },
        "complete_registration:::signed_cr:::waitlist": {
            title: "You have completed the final registration!",
            description:
                "You have been placed on the waitlist. Meanwhile, please make sure to fill in the remaining cards.",
            variant: "success"
        },
        "after_complete_registration:::!signed_cr:::*": {
            title: "The final registration is over",
            description: (
                <>
                    Please contact us at {salesEmail} if you want to participate
                    in this year's event.
                </>
            ),
            variant: "warning"
        },
        "after_complete_registration:::signed_cr:::pending": {
            title: "You have completed the final registration!",
            description:
                "We are currently processing your application. Meanwhile, please make sure to fill in the remaining cards.",
            variant: "success"
        },
        "after_complete_registration:::signed_cr:::accepted": {
            title: "You have completed the final registration!",
            description:
                "You got a spot at the fair! Please make sure to fill in the remaining cards.",
            variant: "success"
        },
        "after_complete_registration:::signed_cr:::waitlist": {
            title: "You have completed the final registration!",
            description:
                "You have been placed on the waitlist. Meanwhile, please make sure to fill in the remaining cards.",
            variant: "success"
        },
        "fair:::!signed_cr:::*": {
            title: "Welcome to Armada!",
            description: (
                <>
                    This years fair is currently underway. We're looking forward
                    to seeing you at next year's event again! If you have any
                    questions, please contact {salesEmail}
                </>
            )
        },
        "fair:::signed_cr:::accepted": {
            title: "See you at the fair!",
            description: (
                <>
                    We're looking forward to seeing you at this year's event. If
                    you have any questions, please contact {salesEmail}
                </>
            ),
            variant: "success"
        },
        "after_fair:::!signed_cr:::*": {
            title: "Welcome to Armada!",
            description: (
                <>
                    We're looking forward to seeing you at next year's event
                    which you can sign up for at {newSignupForm}
                </>
            )
        },
        "after_fair:::signed_cr:::accepted": {
            title: "Thank you for coming to Armada!",
            description: (
                <>
                    We're looking forward to seeing you at next year's event
                    which you can sign up for at {newSignupForm}
                </>
            ),
            variant: "success"
        },
        "*:::*:::pending": {
            title: "We are currently processing your application",
            description: (
                <>
                    Meanwhile, please fill out the available cards. If
                    you have any questions please contact us at {salesEmail}.
                </>
            ),
            variant: "success"
        },
        "*:::*:::waitlist": {
            title: "You have been placed on the waitlist",
            description: (
                <>
                    Meanwhile, please fill out the available cards. If
                    you have any questions please contact us at {salesEmail}.
                </>
            ),
            variant: "success"
        },
        "*:::*:::accepted": {
            title: "Congratulations! You've got a spot at the fair",
            description:
                "We'll be in touch with more information. Meanwhile, please fill out the available forms",
            variant: "success"
        },
        "*:::!signed_ir:::*": {
            title: "Welcome to Armada!",
            description:
                "To get a spot in this year's event, please complete the initial registration"
        }
    }

export function getTimelinePhaseMessage(state: AccessDeclarationArgs | null) {
    return parseAccessDeclaration(state, TIMELINE_STEPS)?.value
}
