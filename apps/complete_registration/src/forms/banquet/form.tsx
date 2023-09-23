import { Form } from "../form_types"
import { CommingSoon } from "../lunch_tickets/comming_soon.page"

export const form: Form = {
    //@ts-ignore
    key: "banquet_tickets",
    name: "Banquet Tickets",
    description:
        "Banquet tickets give attendees access to the the official Armada dinner",
    progression: "none",
    pages: [
        {
            id: "",
            title: "Comming Soon",
            hasNextButton: false,
            hasPrevButton: false,
            pageComponent: CommingSoon
        }
    ]
}
