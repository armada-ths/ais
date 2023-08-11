import { Form } from "../../screens/form/screen"
import { BasicInfoFormPage } from "../exhibitor_catalog/basic_info.page"

const form: Form = {
    key: "lunch_tickets",
    name: "Lunch Tickets",
    description:
        "Lunch tickets give attendees access to the lunch area at the fair",
    isSkippable: true,
    pages: [
        {
            id: "",
            title: "Select Events",
            pageComponent: BasicInfoFormPage
        }
    ]
}
export default form
