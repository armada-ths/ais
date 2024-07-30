import { Checkbox } from "@/components/ui/checkbox"
import { FormWrapper } from "@/forms/FormWrapper"
import { ReactNode } from "react"

function Title({ text }: { text: string }) {
    return <h3 className="mb-2 text-xl capitalize text-emerald-300">{text}</h3>
}

function Link({ children, href }: { children: ReactNode; href: string }) {
    return (
        <a
            href={href}
            className="font-medium text-blue-600 hover:underline dark:text-blue-500"
        >
            {children}
        </a>
    )
}

export function TransportInfoFormPage() {
    return (
        <FormWrapper>
            <div className="mb-5 text-center text-sm">
                <Link href="https://drive.google.com/file/d/1op7D51O0QpOljNQMBP-UscNRpWlRs31X/view?usp=drive_linkhttps://drive.google.com/file/d/1op7D51O0QpOljNQMBP-UscNRpWlRs31X/view?usp=drive_link">
                    Download book transport PDF-form
                </Link>
                <div className="text-xs text-slate-400">(read more below)</div>
            </div>
            <p className="mb-5 text-sm">
                We offer Armada Transport to our exhibitors. This means you can
                enjoy free transport of you goods to and from the fair (up to
                the amount specified below) from any place in Europe!
            </p>
            <p className="mb-5 text-sm">
                This both makes the logistics smoother around the fair and is
                more sustainable; one company transporting goods with fewer
                round trips, rather than letting everyone find their own
                transportation solution leading to a higher climate impact.
            </p>
            <div className="flex flex-col items-center">
                <img
                    style={{ float: "right", maxWidth: "300px" }}
                    src="/static/images/DHL_rgb.png"
                />
                <p className="mb-5 text-center text-sm font-medium">
                    Armada is happy to announce that we are cooperating with DHL
                    this year. All of the administration of bookings will be
                    handled directly by DHL.
                </p>
            </div>
            <p className="mb-5 text-sm">
                In the bronze, silver and gold kits is included one of the
                following transport options to and from the fair free of charge
                within Europe:
            </p>
            <p className="mb-5 text-sm">
                a) Two packages, maximum measures 150x50x50 cm each and maximum
                weight 35 kg each
            </p>
            <p className="mb-5 text-sm">
                b) One half pallet*, maximum measures 60x50x150 cm and maximum
                weight 400 kg
            </p>
            <p className="mb-5 text-sm">
                c) One EUR-pallet* maximum measures 120x80x200 cm and maximum
                weight 950 kg
            </p>
            <p className="mb-5 text-sm">
                d) One cage trolley* maximum measures
            </p>
            <p className="mb-5 text-sm">
                120x80x200 cm and maximum weight 950 kg *Not provided by
                DHL/Armada If none of these options are what you have in mind.
                There is an additional space to add information about your
                specific packaging on the PDF and send it to DHL, they will then
                return with a price for transport. NOTE that this will be billed
                directly by DHL to you as exhibitor. Please observe that only
                bookings made with Armada Transport/DHL will be granted access
                to use the loading dock in the buildings on KTH Campus. This
                means that if you book your own transport with another company
                you will have to carry your own goods through the main entrance.
                This is due to strict limitations of space and accessibility
                around the fair buildings.
            </p>
            <Title text="How to book transport" />
            <p className="mb-5 text-sm">
                To book Armada you need to download{" "}
                <Link href="https://drive.google.com/file/d/1op7D51O0QpOljNQMBP-UscNRpWlRs31X/view?usp=drive_linkhttps://drive.google.com/file/d/1op7D51O0QpOljNQMBP-UscNRpWlRs31X/view?usp=drive_link">
                    download this PDF-form
                </Link>{" "}
                and fill it in with information regarding pickup/return address,
                What type of parcel and the dimensions and weight of your goods.
                After filling in the PDF you should email it directly to DHL on{" "}
                <Link href="booking.armada@dhl.com">
                    booking.armada@dhl.com
                </Link>
                .
            </p>

            <p className="mb-5 text-sm">
                The deadline for booking is the{" "}
                <span className="underline">23rd of October</span>, but do not
                wait until it is too late! The goods must be packed prior to
                week 45
                <span className="underline">(6th of november)</span>. You are
                responsible for packaging the goods, the goods must be able to
                withstand normal handling of goods in the terminal.
            </p>
            <Title text="PACKAGING INSTRUCTIONS" />
            <p className="mb-5 text-sm">
                In order to ensure that all exhibitor goods arrive safely and in
                one piece, it is important that you package your goods
                correctly. See these{" "}
                <Link href="https://drive.google.com/drive/u/0/folders/1JhrN3dzI9X3GvOWtIRgkvIZK8crr1Spu">
                    instructions
                </Link>{" "}
                about packaging tips from DHL for a safe shipment. Please note
                that it is your responsibility to ensure that the goods you are
                sending to and from the fair are packaged correctly according to
                the packaging instructions and labeled at pick-up. If you have
                any questions regarding packing you can contact THS Armada's own
                transport team.
            </p>
            <Title text="EXHIBITING AT BOTH ARKAD AND ARMADA?" />
            <p className="mb-5 text-sm">
                To ensure an easier transition for you exhibiting at ARKAD, that
                takes place a week before ARMADA we have worked together with
                ARKAD to arrange a transport solution for companies that are
                going to be participating at both events. The same options as
                above are also included for transportation of company goods
                between the fairs. To book, get in touch with your contact
                person at ARKAD. If you are uncertain who your contact person is
                email{" "}
                <Link href="mailto:fair.arkad@tlth.se">fair.arkad@tlth.se</Link>{" "}
                and they will sort that out for you
            </p>
            <Title text="Where to turn to?" />
            <p className="mb-5 text-sm">
                If you have any questions regarding booking of transports you
                can email DHL on Email:{" "}
                <Link href="mailto:booking.armada@dhl.com">
                    booking.armada@dhl.com
                </Link>
            </p>
            <p className="mb-5 text-sm">
                Phone: +46 31 363 1185 , +46 363 11 27
            </p>
            <p className="mb-5 text-sm">
                if you have any general questions regarding transport or
                logistics. THS Armada's own transport team will also be at your
                service on Email:{" "}
                <Link href="sustomer.support@armada.nu">sales@armada.nu</Link>
            </p>
            <div className="mt-10 flex flex-1 justify-center">
                <Checkbox />
            </div>
        </FormWrapper>
    )
}
