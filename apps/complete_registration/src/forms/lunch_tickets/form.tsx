import { Form } from "../../screens/form/screen"
import { CommingSoon } from "./comming_soon.page"

const form: Form = {
    key: "lunch_tickets",
    name: "Lunch Tickets",
    description:
        "Lunch tickets give attendees access to the lunch area at the fair",
    progression: "none",
    pages: [
        {
            id: "",
            title: "Select Events",
            hasNextButton: false,
            hasPrevButton: false,
            pageComponent: CommingSoon
        }
    ]
}
export default form
