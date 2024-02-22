import {
    Drawer,
    DrawerClose,
    DrawerContent,
    DrawerDescription,
    DrawerFooter,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger
} from "@/components/ui/drawer"
import { Separator } from "@/components/ui/separator"
import { useDashboard } from "@/shared/hooks/useRegistration"
import { X } from "lucide-react"

export function ContactBubble() {
    const { data } = useDashboard()

    const companyContact = data?.sales_contacts?.[0]
    const additionalCompanyContacts = data?.sales_contacts?.slice(1)

    if (companyContact == null) return null

    return (
        <Drawer>
            <DrawerTrigger>
                <div className="h-20 w-20 overflow-hidden rounded-full transition-all duration-200 active:scale-95">
                    <img
                        src={companyContact.picture_original}
                        className="h-full w-full bg-stone-500"
                    />
                </div>
            </DrawerTrigger>
            <DrawerContent className="mx-auto max-w-[700px] lg:px-8">
                <DrawerClose className="absolute right-4 top-2 rounded-lg bg-stone-200 p-1">
                    <X size={20} className="text-stone-800" />
                </DrawerClose>
                <DrawerHeader className="lg:pt-8">
                    <div className="flex gap-5">
                        <div className="flex-[2]">
                            <DrawerTitle className="text-start">
                                Hi, I'm {companyContact.first_name}
                            </DrawerTitle>
                            <DrawerDescription className="mt-2 text-start">
                                I'm your host at Armada. If you have any
                                questions don't hesitate to contact me!
                                <div className="mt-5 flex flex-col gap-y-2">
                                    <p className="">
                                        Mail:{" "}
                                        <a
                                            href={`mailto:${companyContact.email}`}
                                            className="text-emerald-400 underline hover:cursor-pointer"
                                        >
                                            {companyContact.email}
                                        </a>
                                    </p>
                                    <p className="">
                                        Phone:{" "}
                                        <a
                                            href={`tel:${companyContact.phone_number}`}
                                            className="underline hover:cursor-pointer"
                                        >
                                            {companyContact.phone_number}
                                        </a>
                                    </p>
                                </div>
                            </DrawerDescription>
                        </div>
                        <div className="flex flex-1 justify-end">
                            <div className="aspect-square h-full max-h-20 overflow-hidden rounded-full">
                                <img
                                    src={companyContact.picture_original}
                                    className="h-full w-full bg-stone-500"
                                />
                            </div>
                        </div>
                    </div>
                </DrawerHeader>
                {additionalCompanyContacts != null &&
                    additionalCompanyContacts.length > 0 && (
                        <>
                            <Separator className="mt-5" />
                            <DrawerFooter>
                                <DrawerTitle>Secondary Contacts</DrawerTitle>
                                <div className="flex flex-wrap justify-between gap-4">
                                    {additionalCompanyContacts.map(contact => (
                                        <div>
                                            <p className="text-sm">
                                                {contact.first_name} -{" "}
                                                {contact.title}
                                            </p>
                                            <DrawerDescription>
                                                <a
                                                    href={`mailto:${companyContact.email}`}
                                                    className="text-stone-400 underline hover:cursor-pointer"
                                                >
                                                    {companyContact.email}
                                                </a>
                                            </DrawerDescription>
                                        </div>
                                    ))}
                                </div>
                            </DrawerFooter>
                        </>
                    )}
            </DrawerContent>
        </Drawer>
    )
}
