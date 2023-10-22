import { useEffect, useState} from "react"
import { useSelector } from "react-redux"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { FormWrapper } from "../FormWrapper"
import { Dropdown } from 'primereact/dropdown';
import LunchTicketView from "./lunch_tickets"
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils"
import './lunch_ticket.css'

export function ViewLunchTicketsPage() {
    const result = useSelector((state: RootState) =>
        selectField(state, "result")
    )
    const tickets : LunchTicket[] = result?.value as LunchTicket[];
    const [shownTickets, setShownTickets] = useState<LunchTicket[]>(tickets);
    const [filterUsedState, setFilterUsedState] = useState<string>("All");
    const [filterDateState, setFilterDateState] = useState<string>("Any");

    // This should not be here... FIXUP LATER (move into redux state)
    useEffect(() => {
        if(shownTickets == null)
            setShownTickets(tickets);
        searchTickets();
    }, [])

    const searchTickets = () => {
        //Filter tickets
        if(tickets.length > 0){
            const filteredTickets = tickets.filter((ticket: LunchTicket) => {
                if (filterUsedState == 'All' || (ticket.used && filterUsedState == 'Used') || (!ticket.used && filterUsedState == 'Available')) {
                    if(filterDateState ==='Any' || ticket.day.includes(filterDateState))
                        return ticket;
                }
                return false;
            });
            //update
            setShownTickets(filteredTickets as LunchTicket[]);
        }
    }


    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700 max-w-md">
            <h2 className="font-bold text-md text-center">Here you can find all your lunch tickets</h2>
            <form className="flex w-lg" >
                <div className="w-1/3 mr-auto">
                    <label htmlFor="used-tickets" className="pr-2">Ticket Status:</label>
                    <Dropdown value={filterUsedState} onChange={(event) => {
                        setFilterUsedState(event.value);
                    }} options={['All', 'Available', 'Used']} className="w-full md:w-14rem" />
                </div>
                <div className="w-1/3">
                    <label htmlFor="ticket-date" className="pr-2">Ticket date:</label>
                    <Dropdown value={filterDateState} onChange={(event) => {
                        setFilterDateState(event.value);
                    }} options={['Any', '2023-11-21', '2023-11-22']} className="w-full md:w-14rem" />
                </div>
            </form>
            {shownTickets.map((ticket, index) => {
                return (
                    <div key={index} className="+mb-6 min-w-75">
                        <LunchTicketView key={index} ticket={ticket} ></LunchTicketView>
                    </div>
                );
            })}
            {(shownTickets.length == 0 ?
                <p className="font-semibold pt-4 text-center">No tickets found under your company.</p>
                :
                ""
            )}
        </FormWrapper>
    )
}
