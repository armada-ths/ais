import { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { FormWrapper } from "../FormWrapper"
import { Dropdown } from 'primereact/dropdown';

import './lunch_ticket.css'

interface LunchTicket{
    id: string;
    name: string;
    email_address: string;
    comment: string;
    date: string;
    used: boolean;
    type: string;
    dietary_restrictions: [];
    other_dietary_restrictions: string;
}

export function ViewLunchTicketsPage() {
    const result = useSelector((state: RootState) =>
        selectField(state, "result")
    )
    const tickets : LunchTicket[] = result?.value as LunchTicket[];
    const [shownTickets, setShownTickets] = useState<LunchTicket[]>(tickets);
    const [usedFormState, setUsedFormState] = useState<string>("all");
    // This should not be here... FIXUP LATER (move into redux state)
    useEffect(() => {
        if(shownTickets == null)
            setShownTickets(tickets);
    }, [tickets])

    const searchTickets = () => {
        const usedSelect = document.getElementById('used-tickets') as HTMLSelectElement;
        const dateSelect = document.getElementById('ticket-date') as HTMLSelectElement;

        const used = usedFormState;
        const date = dateSelect.value

        //Filter tickets
        const filteredTickets = tickets.filter((ticket: LunchTicket) => {
            if (used == 'all' || (ticket.used && used == 'used') || (!ticket.used && used == 'available')) {
                if(date ==='any' || ticket.date.includes(date))
                    return ticket;
            }
            return false;
        });

          //update
        setShownTickets(filteredTickets as LunchTicket[]);
    }

    const displayDietaryRestrictions = (event: any) => {
        const dietaryRestrictionsDiv = event.target.closest('.dietary-restrictions-container');
        const dietaryRestrictionsList = dietaryRestrictionsDiv.querySelector('.dietary-restrictions');

        if (dietaryRestrictionsList) {
            // Toggle the visibility of the closest 'dietary-restrictions' div
            const currentDisplay = dietaryRestrictionsList.style.display;
            dietaryRestrictionsList.style.display = currentDisplay === 'none' ? 'grid' : 'none';
        }
    }

    if (shownTickets == null) return null

    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <h2 className="font-bold text-md text-center">Here you can find all your lunch tickets</h2>
            <form className="flex">
                <div className="grow">
                    <label htmlFor="used-tickets" className="pr-2">Ticket Status:</label>
                    <Dropdown value={usedFormState} onChange={(event) => {
                        searchTickets();
                        setUsedFormState(event.value);
                    }} options={['all', 'available', 'used']} className="w-full md:w-14rem" />
                    <select id="used-tickets" name="used-tickets" className="border-solid border-2" onChange={searchTickets}>
                        <option value="all">All</option>
                        <option value="available">Available</option>
                        <option value="used">Used</option>
                    </select>
                </div>
                <div className="grow">
                    <label htmlFor="ticket-date" className="pr-2">Ticket date:</label>
                    <select id="ticket-date" name="ticket-date" className="border-solid border-2" onChange={searchTickets}>
                        <option value="any">Any</option>
                        <option value="2023-11-21">21 Nov</option>
                        <option value="2023-11-22">22 Nov</option>
                    </select>
                </div>
            </form>
            {shownTickets.map((ticket, index) => {
                return (
                    <div key={index} className="+mb-6">
                    <div className="lunch-ticket border-solid border-2 border-b-0">
                        <div className="flex w-full pt-2 pb-4 pl-4 pr-4">
                            <p className="text-xl mb-5 grow font-bold">Lunch ticket</p>
                            <div className="text-right grow font-semibold">
                                <p>{ticket.date.split(" ")[0]}</p>
                                <p>{ticket.date.split(" ")[1]}</p>
                            </div>
                        </div>
                        <div className="flex pl-4 pb-1">
                            <div className={"lunch-ticket-availability" + ((ticket.used ? " used" : ""))} />
                            <p className="pl-2 font-semibold">{(ticket.used ? 'Used' : 'Assigned')}</p>
                        </div>
                        <div className="dietary-restrictions-container">
                            <button className="w-full border-t-2 border-b-2 flex justify-center cursor-pointer" onClick={displayDietaryRestrictions}>
                                <span>Dietary Restrictions</span>
                                <img src="/chevron_down_icon.svg" className="pl-2" alt="Chevron Down" />
                            </button>
                            <div className="dietary-restrictions grid grid-cols-2 gap-4 text-center [&>*]:pt-2 border-b-2 pb-2" style={{display: 'none'}}>
                                {ticket.dietary_restrictions.map((dietary_restriction) => {return(<p>{dietary_restriction}</p>)})}
                                <p style={{ display: (ticket.dietary_restrictions.length > 0 ? "none" : "block")}}>No dietary restrictions</p>
                            </div>
                        </div>
                    </div>
                    </div>
                );
                })}
        </FormWrapper>
    )
}
