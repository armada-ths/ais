import React from "react"
import { FormWrapper } from "../FormWrapper"
import { CompleteButton } from "../../shared/CompleteButton"

export function LinkText({ children }: { children: React.ReactNode }) {
    return <p className="font-semibold text-blue-600">{children}</p>
}

export function StureContactPage() {
    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <img
                draggable={false}
                className="my-5 h-72 select-none object-contain"
                src={"/static/images/sture_skolden_cmyk_75mm_bred.png"}
            />
            <p>
                Armada are pleased to once again present Sture™ as our fair
                partner. Sture can help you with all contents for your booth and
                make it stand out in a great way. They are on the frontier of
                fair furnishings both when it comes to technologies and
                sustainable production - a perfect fit for your Armada booth!
            </p>
            <p>
                You can find their contact information below - we really
                recommend talking to them about how your booth can really stand
                out on the fair!
            </p>
            <p className="-mx-8 rounded bg-slate-300 p-5 px-8 text-slate-900">
                Sture™ är en totalleverantör och produktionsbyrå inom
                varumärkesmiljöer. Vi skapar kreativa koncept för mässor,
                montrar, events, interiör, display. Företaget grundades 1945 och
                vi har vår produktionsanläggning i Järfälla. Vi har samarbetat
                med Armada under många år och hälsar nya som gamla kunder till
                oss för att förutsättningslöst diskutera olika förslag.
            </p>
            <div>
                <p className="mb-2">
                    Frågor rörande bokning av befintliga paket eller hyra av
                    möbler/grafik, kontakta:
                </p>
                <p className="flex gap-2">
                    <LinkText>louise.jernstrom@sture.se</LinkText>
                </p>
                <p className="flex gap-2">
                    Mobile: <LinkText>+46 76 526 59 43</LinkText>
                </p>
            </div>

            <div className="mt-5">
                <p className="mb-2">
                    Vid frågor rörande köp av monterväggar (ljuslådor, pop-ups
                    etc) alternativt helhetslösningar, kontakta:
                </p>
                <LinkText>mats.svensson@sture.se</LinkText>
                <div></div>
                <p className="flex gap-2">
                    Direct: <LinkText>+46 8 586 159 30</LinkText>
                </p>
                <p className="flex gap-2">
                    Mobile: <LinkText>+46 76 526 59 30</LinkText>
                </p>
            </div>

            <div className="mt-5 text-center">
                <CompleteButton text="Return back" />
            </div>
        </FormWrapper>
    )
}
