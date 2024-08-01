import { Card, CardContent } from "@/components/ui/card"
import { FormWrapper } from "../FormWrapper"
import { Button } from "@/components/ui/button"
import { ExternalLinkIcon } from "lucide-react"

export function DiversityIndexPage() {
    return (
        <FormWrapper>
            <div className="flex flex-col">
                <Card className="p-7 text-justify [&>p]:mb-5 max-w-screen-md">
                    <CardContent className="flex flex-col gap-4 py-3">
                        <p>Hi,</p>
                        <p>
                            {" "}
                            <b>Diversity has become an important aspect</b> people look
                            for when starting their careers. Here at Armada we have
                            prepared a survey that will make it easier for the students
                            at KTH to determine the role that diversity plays at your
                            company along with the steps you take to boost inclusivity
                            at your workplace.
                        </p>
                        <p>
                            {" "}
                            You <b>can answer the survey before 29/9 </b>to give the
                            students at one of Europe’s leading technical universities a
                            chance to get to know your values. You are free to skip
                            questions.
                        </p>
                        <p>
                            {" "}
                            The results of the survey, together with our own research
                            will decide which companies we{" "}
                            <u>select for the diversity focus room</u>. Specific{" "}
                            <b>results will not be shared</b> with anyone outside of
                            Armada.
                        </p>
                        <p> Thank you in advance!</p>
                        <p>
                            {" "}
                            <b>Armada Diversity Team</b>
                        </p>
                    </CardContent>
                </Card>
                <div className="mt-8 text-center">
                    <a
                        className="text-bold rounded-md border-solid p-3 text-lg font-semibold text-blue-600 underline visited:text-purple-600 hover:text-blue-800"
                        href="https://docs.google.com/forms/d/1NtomBDMyU3WHsIXC30jLsh8Ym5bQdNv7C1LGH5Nlv_U/viewform?pli=1&pli=1&edit_requested=true"
                        target="_blank"
                    >
                        <Button className="inline-flex gap-2">
                            <span>Go to the Diversity Form</span>
                            <ExternalLinkIcon />
                        </Button>
                    </a>
                </div>
            </div>
        </FormWrapper>
    )
}
