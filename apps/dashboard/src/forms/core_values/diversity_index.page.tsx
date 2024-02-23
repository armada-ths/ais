import { FormWrapper } from "../FormWrapper"

export function DiversityIndexPage() {
    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <div className="border-solid border-2 border-slate-300 p-7 text-justify [&>p]:mb-5">
                <p> Hi,</p>
                <p> <b>Diversity has become an important aspect</b> people look for when starting their careers. Here at Armada we have prepared a survey that will make it easier for the students at KTH to determine the role that diversity plays at your company along with the steps you take to boost inclusivity at your workplace.</p>
                <p> You <b>can answer the survey before 29/9 </b>to give the students at one of Europe’s leading technical universities a chance to get to know your values. You are free to skip questions.</p>
                <p> The results of the survey, together with our own research will decide which companies we <u>select for the diversity focus room</u>. Specific <b>results will not be shared</b> with anyone outside of Armada.</p>
                <p> Thank you in advance!</p>
                <p> <b>Armada Diversity Team</b></p>
            </div>
            <div className="mt-3 text-center">
                <a className="underline text-bold text-lg border-solid rounded-md p-3 font-semibold text-blue-600 hover:text-blue-800 visited:text-purple-600" href="https://docs.google.com/forms/d/1NtomBDMyU3WHsIXC30jLsh8Ym5bQdNv7C1LGH5Nlv_U/viewform?pli=1&pli=1&edit_requested=true">Go to the Diversity Form </a>
            </div>

        </FormWrapper>
    )
}
