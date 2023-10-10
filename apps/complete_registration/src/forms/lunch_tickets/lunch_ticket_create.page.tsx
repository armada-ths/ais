import { useSelector } from "react-redux"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { FormWrapper } from "../FormWrapper"
import './lunch_ticket.css'

export function CreateLunchTicketsPage() {
    const transportTo = useSelector((state: RootState) =>
        selectField(state, "exhibitor.transport_to")
    )   
    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <h2 className="font-bold text-md text-center">Here you can create your lunch tickets</h2>
            <form className="flex flex-col [&>label]:font-bold [&>label]:pt-4">
                <label htmlFor="ticket-date" className="pr-2">Day:</label>
                <select id="ticket-date" name="ticket-date" className="border-solid border-2">
                    <option value="any">Any</option>
                    <option value="21">21 Nov</option>
                    <option value="22">22 Nov</option>
                </select>
                <label htmlFor="ticket-date" className="pr-2">Timeslot:</label>
                <select id="ticket-date" name="ticket-date" className="border-solid border-2">
                    <option value="11">11:00</option>
                    <option value="11.30">11:30</option>
                    <option value="12">12:00</option>
                    <option value="12.30">12:30</option>
                    <option value="13">13:00</option>
                    <option value="13.30">13:30</option>
                    <option value="14">14:00</option>
                </select>
                <label htmlFor="dietary-restrictions" className="pr-2">Dietary restrictions:</label>
                <div id="dietary-restrictions-list" className="grid grid-cols-2 [&>div]:pt-2">
                        <div>
                            <input type="checkbox"/>Apples
                        </div>
                        <div>
                            <input type="checkbox"/>Avocado
                        </div>
                        <div>
                            <input type="checkbox"/>Beef
                        </div>
                        <div>
                            <input type="checkbox"/>Eggs
                        </div>
                </div>
                <label htmlFor="other-dietary-restrictions" className="pr-2 block">Other dietary restrictions</label>
                <input className="border-solid border-2" placeholder="Other dietary restrictions" type="text" name="other-dietary-restrictions" required/>
                <label htmlFor="other-comments" className="pr-2 block">Other comments</label>
                <input className="border-solid border-2" placeholder="Your comment" type="text" name="other-comments" required/>
                <button className="m-auto mt-4 pt-2 pb-2 bg-indigo-500 rounded-md w-2/4 text-white">Create lunch ticket</button>
            </form>
        </FormWrapper>
    )
}
