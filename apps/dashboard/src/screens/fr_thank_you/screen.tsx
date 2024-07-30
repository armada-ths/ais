import ArmadaLogoGreen from "@/assets/armada_logo_green.svg"
import { InfoScreen } from "@/shared/InfoScreen"
import { Link } from "@tanstack/react-router"
import { DateTime } from "luxon"

function TextSection({ children }: { children: React.ReactNode }) {
    return <p className="mt-4 text-slate-500">{children}</p>
}

export function FinalRegistrationThankYouScreen() {

    return (
        <div className="my-20 flex flex-col items-center justify-center">
            <div className="mb-5 h-24 w-24">
                <img src={ArmadaLogoGreen} />
            </div>
            <InfoScreen title="You're in!" link={null} fullscreen={false}>
                <div className="mt-5">
                    <TextSection>
                        Thank you for compleating the final registration and
                        welcome to Armada! You have gotten an email to{" "}
                        <a
                            href={`mailto:${user?.email_address}`}
                            className="text-blue-500 underline"
                        >
                            {user?.email_address}
                        </a>{" "}
                        confirming your Final Registration.
                    </TextSection>
                    <TextSection>
                        Your next step is to complete all the cards in the
                        dashboard by{" "}
                        <b>
                            {DateTime.fromObject({
                                month: 9,
                                day: 28
                            })
                                .plus({ weeks: 3 })
                                .toFormat("dd MMMM")}
                        </b>
                        . Do not hesitate To contact us at{" "}
                        <a
                            href="mailto:sales@armada.nu"
                            className="text-blue-500 underline"
                        >
                            sales@armada.nu
                        </a>{" "}
                        with any questions!
                    </TextSection>
                    <TextSection>
                        Your host will be in touch with you in October to help
                        out with any questions leading up to the fair. If you've
                        ordered events the event team will also be in touch!
                    </TextSection>
                    <TextSection>
                        Thank you again for joining us this year and we hope you
                        will have a great Armada!
                    </TextSection>
                    <div className="mt-5 italic text-slate-400">
                        // The whole THS Armada team and the KTH students
                    </div>
                    <div className="mt-10 flex justify-center">
                        <Link
                            replace
                            className="text-slate-500 underline"
                            to="/"
                        >
                            Return to dashboard
                        </Link>
                    </div>
                </div>
            </InfoScreen>
        </div>
    )
}
