import { Form } from "../../screens/form/screen"
import { CommingSoon } from "../lunch_tickets/comming_soon.page"

export const form: Form = {
    key: "banquet_tickets",
    name: "Banquet Tickets",
    description:
        "Banquet tickets give attendees access to the the official Armada dinner",
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
