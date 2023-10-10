import { useSelector } from "react-redux"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { FormWrapper } from "../FormWrapper"
import './lunch_ticket.css'

export function ViewLunchTicketsPage() {
    const transportTo = useSelector((state: RootState) =>
        selectField(state, "exhibitor.transport_to")
    )   
    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <h2 className="font-bold text-md text-center">Here you can find all your lunch tickets</h2>
            <p>{transportTo?.value?.toString() ?? "unknown"}</p>
            <form className="flex">
                <div className="grow">
                    <label htmlFor="used-tickets" className="pr-2">Ticket Status:</label>
                    <select id="used-tickets" name="used-tickets" className="border-solid border-2">
                        <option value="all">All</option>
                        <option value="available">Available</option>
                        <option value="used">Used</option>
                    </select>
                </div>
                <div className="grow">
                    <label htmlFor="ticket-date" className="pr-2">Ticket date:</label>
                    <select id="ticket-date" name="ticket-date" className="border-solid border-2">
                        <option value="any">Any</option>
                        <option value="21">21 Nov</option>
                        <option value="22">22 Nov</option>
                    </select>
                </div>
            </form>
            
            <div className="[&>*]:mb-6">
                <div className="lunch-ticket border-solid border-2 border-b-0">
                    <div className="flex w-full pt-2 pb-4 pl-4 pr-4">
                        <p className="text-xl mb-5 grow font-bold">Lunch ticket</p>
                        <div className="text-right grow font-semibold">
                            <p>01/01/2000</p>
                            <p>00:00</p>
                        </div>
                    </div>
                    <div className="flex pl-4 pb-1">
                        <div className="lunch-ticket-availability"/>
                        <p className="pl-2 font-semibold">Assigned</p>
                    </div>
                    <div className="w-full border-t-2 border-b-2 flex justify-center cursor-pointer" >
                        <span>Dietary Restrictions</span>
                        <img src='/chevron_down_icon.svg' className="pl-2"></img>
                    </div>
                    <div className="dietary-restrictions grid grid-cols-2 gap-4 text-center [&>*]:pt-2 border-b-2 pb-2">
                            <p>Restriction 1</p>
                            <p>Restriction 2</p>
                    </div>
                </div>

                <div className="lunch-ticket border-solid border-2 border-b-0">
                    <div className="flex w-full pt-2 pb-4 pl-4 pr-4">
                        <p className="text-xl mb-5 grow font-bold">Lunch ticket</p>
                        <div className="text-right grow font-semibold">
                            <p>01/01/2000</p>
                            <p>00:00</p>
                        </div>
                    </div>
                    <div className="flex pl-4 pb-1">
                        <div className="lunch-ticket-availability used"/>
                        <p className="pl-2 font-semibold">Used</p>
                    </div>
                    <div className="w-full border-t-2 border-b-2 flex justify-center cursor-pointer" >
                        <span>Dietary Restrictions</span>
                        <img src='/chevron_down_icon.svg' className="pl-2"></img>
                    </div>
                    <div className="dietary-restrictions grid grid-cols-2 gap-4 text-center [&>*]:pt-2 border-b-2 pb-2">
                            <p>Restriction 1</p>
                            <p>Restriction 2</p>
                    </div>
                </div>
            </div>
        </FormWrapper>
    )
}
