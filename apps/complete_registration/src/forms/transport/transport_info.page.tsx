import { FormWrapper } from "../FormWrapper"
import { FormField } from "../../screens/form/FormInput"
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
                <Link href="https://drive.google.com/file/d/1pgUdfE9IM3zEuKVuL8XYmviRWqd9y284/view?usp=sharing">
                    Download book transport PDF-form
                </Link>
                <div className="text-xs text-slate-400">(read more below)</div>
            </div>
            <p className="mb-5 text-sm">
                This year Armada is proud to present the concept Armada
                Transport which includes free transportation (limitations apply
                below) of your goods to and from the fair. The background behind
                offering this service is our aim to reduce Armada's impact on
                the environment and ensure a smooth exhibitor experience. We
                believe that it is more sustainable to have one transportation
                company transporting goods with a fewer amount of trucks driving
                on the road, rather than letting everyone find their own
                transportation solution leading to a higher climate impact with
                more trucks driving to KTH and more complex logistics.
            </p>
            <img
                style={{ float: "right", maxWidth: "300px" }}
                src="/static/images/DHL_rgb.png"
            />
            <p className="mb-5 text-sm">
                Armada is happy to announce that we have hired DHL to handle the
                transportation. All of the administration of bookings will be
                handled directly by DHL. Included in the Base kit are some free
                transportation options, which gives you the opportunity to
                choose one of the following options for transports within Europe
                to and from the fair without any extra costs:
            </p>
            <p className="mb-5 text-sm">
                a) Two packages, maximum measures 150x50x50 cm each and maximum
                weight 35 kg each
            </p>
            <p className="mb-5 text-sm">
                b) One half pallet, maximum measures 60x50x150 cm and maximum
                weight 400 kg
            </p>
            <p className="mb-5 text-sm">
                c) One EUR-pallet maximum measures 120x80x200 cm and maximum
                weight 950 kg (the EUR-pallet is not provided by DHL/Armada)
            </p>
            <p className="mb-5 text-sm">
                d) One cage trolley maximum measures 120x80x200 cm and maximum
                weight 950 kg (the cage trolley is not provided by DHL/Armada)
            </p>
            <p className="mb-5 text-sm">
                All exhibitors who wants to send something bulky or more goods
                than what is included in one of the options above has to
                negotiate a price directly with DHL by filling in goods
                information in the linked booking PDF below and emailing it to
                DHL. They will then return with a price for transport. This will
                be billed directly by DHL to the concerning exhibitor. Please
                note that only bookings made through our Armada Transport form
                to DHL will be granted access to use the loading dock in the
                buildings on KTH Campus. This means you will not be able to hire
                your own transportation company unless you have the capability
                to carry your goods in by hand through the main entrance. This
                is due to strict limitation of space and accessibility in the
                fair buildings.
            </p>
            <Title text="How to book transport" />
            <p className="mb-5 text-sm">
                The booking system for transportation of booth goods to and from
                the fair is now open! In order to book transport you should{" "}
                <Link href="https://drive.google.com/file/d/1pgUdfE9IM3zEuKVuL8XYmviRWqd9y284/view?usp=sharing">
                    download this PDF-form
                </Link>{" "}
                and fill it in with information regarding pickup/return address,
                which transportation alternative you wish to book and the
                dimensions and weight of your goods. After filling in the PDF
                you should email it directly to DHL on{" "}
                <Link href="tfe.sweden@dhl.com">tfe.sweden@dhl.com</Link>. The
                deadline for booking is the 4th of November, but do not wait
                until it is too late! The goods must be packed prior to DHL’s
                pick-up and you are responsible for packaging the goods, the
                goods must be able to withstand normal handling of goods in
                terminal. If you have any questions regarding booking of
                transports you can email DHL on{" "}
                <Link href="tfe.sweden@dhl.com">tfe.sweden@dhl.com</Link> or
                call them at{" "}
                <Link href="tel:+46 31 799 4773">+46 31 799 4773</Link>. THS
                Armada's own transport team will also be at your service on{" "}
                <Link href="transport@armada.nu">transport@armada.nu</Link> if
                you have any general questions regarding transport or logistics.
            </p>
            <Title text="PACKAGING INSTRUCTIONS" />
            <p className="mb-5 text-sm">
                In order to ensure that all exhibitor goods arrives safely and
                in one piece, it is important that you package your goods
                correctly. See this instruction for packaging tips from DHL for
                a safe shipment. Please note that it is under your
                responsibility to ensure that the goods you are sending to and
                from the fair are packaged correctly according to the packaging
                instructions and labelled at pick-up. If you have any questions
                regarding how you should pack your goods, please ask for further
                help and we will be at your service!
            </p>
            <Title text="EXHIBITING AT BOTH ARKAD AND ARMADA?" />
            <p className="mb-5 text-sm">
                ARKAD is Lunds Tekniska Högskola equivalent to THS Armada and is
                taking place just a week before Armada. Therefore, we have
                together with ARKAD arranged a transportation opportunity for
                companies exhibiting at both events. The same options as above
                are also included for transportation of company goods between
                the fairs. Please get in touch with your contact person at ARKAD
                in order to book this. Email{" "}
                <Link href="fair.arkad@tlth.se">fair.arkad@tlth.se</Link> if you
                are uncertain who your contact person is at ARKAD.
            </p>
            <div className="mt-10 flex flex-1 justify-center">
                <FormField.Checkbox
                    label="I have read and understood this"
                    mapping="exhibitor.transport_information_read"
                />
            </div>
        </FormWrapper>
    )
}
