import { FormWrapper } from "@/forms/FormWrapper"
import { ReactNode } from "react"
// import { DHLForm } from "@/forms/transport/DHLForm"
import { Card, CardContent } from "@/components/ui/card"
import {
    CheckIcon,
    DownloadIcon,
    Loader2,
    MailIcon,
    PhoneIcon
} from "lucide-react"
import { Alert } from "@/components/ui/alert"
import { useMutation } from "@tanstack/react-query"
import { useParams } from "@tanstack/react-router"
import { HOST } from "@/shared/vars"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import clsx from "clsx"

function Title({ text }: { text: string }) {
    return (
        <h3
            className="mb-2 mt-7 w-full text-xl capitalize"
            style={{
                color: "#61d496"
            }}
        >
            {text}
        </h3>
    )
}

function Link({
    children,
    href,
    target
}: {
    children: ReactNode
    href: string
    target?: string
}) {
    return (
        <a
            href={href}
            target={target}
            className="font-medium text-blue-600 hover:underline dark:text-blue-500"
        >
            {children}
        </a>
    )
}

function LinkWithIcon({
    children,
    icon,
    href,
    iconAfterContent,
    target
}: {
    children?: ReactNode
    icon?: ReactNode
    href: string
    target?: string
    iconAfterContent?: boolean
}) {
    return (
        <Link target={target} href={href}>
            <div className="inline-flex cursor-pointer items-center gap-2 hover:underline">
                {!iconAfterContent && icon}
                <span>{children === undefined ? href : children}</span>
                {iconAfterContent && icon}
            </div>
        </Link>
    )
}

function ActionItem({ children, i }: { children: ReactNode; i: number }) {
    return (
        <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-200 text-2xl font-bold text-slate-600">
                {i}
            </div>
            <div className="text-lg font-medium">{children}</div>
        </div>
    )
}

export function TransportInfoFormPage() {
    const { companyId } = useParams({
        from: "/$companyId/form/$formKey/$formPageKey"
    })

    const { data, isPending: isPendingDashboard, invalidate } = useDashboard()

    const { mutate: updateTransportInfo, isPending: isPendingMutation } =
        useMutation({
            mutationFn: async (transport_information_read: boolean) =>
                fetch(`${HOST}/api/dashboard/${companyId}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        exhibitor: {
                            transport_information_read
                        }
                    })
                }),
            onSuccess: async response => {
                invalidate()

                if (response.status >= 200 && response.status < 300)
                    toast.success("Successfully marked transport as done!")
                else {
                    toast.error("Failed to update transport details", {
                        description: JSON.stringify(await response.json())
                    })
                }
            }
        })

    const pending = isPendingDashboard || isPendingMutation
    // Todo: remove any
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const isDone = (data?.exhibitor as any)?.transport_information_read

    return (
        <FormWrapper>
            <Card>
                <CardContent className="max-w-2xl text-sm">
                    <Title text="How to book transport" />
                    <div className="mb-10 mt-8 flex flex-col gap-5 pl-5">
                        <ActionItem i={1}>
                            <LinkWithIcon
                                href="/static/THS_Armada_2023_Logistics.pdf"
                                icon={<DownloadIcon />}
                            >
                                Download the DHL form
                            </LinkWithIcon>
                        </ActionItem>
                        <ActionItem i={2}>
                            Email the filled out form to{" "}
                            <LinkWithIcon
                                href="mailto:booking.armada@dhl.com"
                                icon={<MailIcon />}
                                iconAfterContent
                            >
                                booking.armada@dhl.com
                            </LinkWithIcon>
                        </ActionItem>
                        <ActionItem i={3}>
                            <div className="flex items-center gap-2">
                                After you have sent the email:
                                <Button
                                    variant="secondary"
                                    className={clsx("flex gap-2", {
                                        "bg-green-300": isDone,
                                        "text-black": isDone
                                    })}
                                    onClick={() => updateTransportInfo(true)}
                                    disabled={pending || isDone}
                                >
                                    {pending ? <Loader2 /> : <CheckIcon />}
                                    {isDone ? "Done" : "Mark as done"}
                                </Button>
                            </div>
                        </ActionItem>
                    </div>

                    <p className="mb-5">
                        The deadline for booking is the <b>21st of October</b>,
                        but do not wait until it is too late! The goods must be
                        packed prior to week 45 (<b>6th of november</b>). You
                        are responsible for packaging the goods, the goods must
                        be able to withstand normal handling of goods in the
                        terminal.
                    </p>
                    <Title text="What is Armada Transport?" />
                    <p className="mb-7">
                        Take advantage of our Armada Transport service,
                        providing free transportation of your goods to and from
                        the fair from any location in Europe (up to the
                        specified limit below). This service not only simplifies
                        logistics but also promotes sustainability by reducing
                        the number of transport trips and minimizing the overall
                        climate impact.
                    </p>

                    <Alert className="mb-7">
                        <div className="flex flex-col items-center">
                            <img
                                className="mb-3"
                                style={{ float: "right", maxWidth: "300px" }}
                                src="https://ais.armada.nu/static/images/DHL_rgb.png"
                            />
                            <p className="text-center font-medium">
                                We are pleased to partner with DHL this year.
                                All bookings and administrative tasks will be
                                managed directly by DHL, ensuring a seamless
                                experience for you.
                            </p>
                        </div>
                    </Alert>

                    <p className="mb-5">
                        In the bronze, silver and gold kits is included one of
                        the following transport options to and from the fair
                        free of charge within Europe:
                    </p>
                    <ul className="mb-5 list-inside list-[lower-alpha]">
                        <li>
                            Two packages, maximum measures 150x50x50 cm each and
                            maximum weight 35 kg each.
                        </li>
                        <li>
                            One half pallet*, maximum measures 60x50x150 cm and
                            maximum weight 400 kg.
                        </li>
                        <li>
                            One EUR-pallet* maximum measures 120x80x200 cm and
                            maximum weight 950 kg.
                        </li>
                        <li>One cage trolley* maximum measures.</li>
                    </ul>
                    <p className="mb-5 text-xs text-slate-400">
                        120x80x200 cm and maximum weight 950 kg *Not provided by
                        DHL/Armada If none of these options are what you have in
                        mind. There is an additional space to add information
                        about your specific packaging on the PDF and send it to
                        DHL, they will then return with a price for transport.
                        NOTE that this will be billed directly by DHL to you as
                        exhibitor. Please observe that only bookings made with
                        Armada Transport/DHL will be granted access to use the
                        loading dock in the buildings on KTH Campus. This means
                        that if you book your own transport with another company
                        you will have to carry your own goods through the main
                        entrance. This is due to strict limitations of space and
                        accessibility around the fair buildings.
                    </p>

                    <Title text="Packaging Instructions" />
                    <p className="mb-5">
                        In order to ensure that all exhibitor goods arrive
                        safely and in one piece, it is important that you
                        package your goods correctly. See these{" "}
                        <Link href="https://drive.google.com/drive/u/0/folders/1JhrN3dzI9X3GvOWtIRgkvIZK8crr1Spu">
                            instructions
                        </Link>{" "}
                        about packaging tips from DHL for a safe shipment.
                        Please note that it is your responsibility to ensure
                        that the goods you are sending to and from the fair are
                        packaged correctly according to the packaging
                        instructions and labeled at pick-up. If you have any
                        questions regarding packing you can contact THS Armada's
                        own transport team.
                    </p>
                    <Title text="Exhibiting at both Arkad and Armada?" />
                    <p className="mb-5">
                        To ensure an easier transition for you exhibiting at
                        ARKAD, that takes place a week before ARMADA we have
                        worked together with ARKAD to arrange a transport
                        solution for companies that are going to be
                        participating at both events. The same options as above
                        are also included for transportation of company goods
                        between the fairs. To book, get in touch with your
                        contact person at ARKAD. If you are uncertain who your
                        contact person is, email Arkad's Fair Coordinator:
                    </p>
                    <p className="mb-5">
                        <LinkWithIcon
                            href="mailto:fair.arkad@tlth.se"
                            icon={<MailIcon />}
                        >
                            fair.arkad@tlth.se
                        </LinkWithIcon>
                    </p>
                    <Title text="Where to turn to?" />
                    <p className="mb-5">
                        If you have any questions regarding booking of
                        transports you can email DHL on Email:{" "}
                    </p>
                    <p className="mb-5">
                        <LinkWithIcon
                            href="mailto:booking.armada@dhl.com"
                            icon={<MailIcon />}
                        >
                            booking.armada@dhl.com
                        </LinkWithIcon>
                    </p>
                    <p className="mb-5">
                        If you have any general questions regarding transport or
                        logistics. THS Armada's own transport team will also be
                        at your service on email:
                    </p>
                    <p className="mb-3">
                        <LinkWithIcon
                            href="mailto:ellen.chen@armada.nu"
                            icon={<MailIcon />}
                        >
                            ellen.chen@armada.nu
                        </LinkWithIcon>
                    </p>
                    <p>
                        <LinkWithIcon
                            href="tel:+46700468901"
                            icon={<PhoneIcon />}
                        >
                            +4670 04 68 901 (Ellen Chen, Head of Logistics)
                        </LinkWithIcon>
                    </p>
                </CardContent>
            </Card>
        </FormWrapper>
    )
}
