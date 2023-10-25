import { useEffect, useState } from "react"
import { useSelector } from "react-redux"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { FormWrapper } from "../FormWrapper"
import { Dropdown } from "primereact/dropdown"
import LunchTicketView from "./lunch_tickets"
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils"
import "./lunch_ticket.css"

export function ViewLunchTicketsPage() {
    const result_tickets = useSelector((state: RootState) =>
        selectField(state, "assigned_lunch_tickets")
    );
    const result_fair_days = useSelector((state: RootState) =>
        selectField(state, "fair_days")
    );

    const tickets = (result_tickets?.value ?? []) as LunchTicket[]
    const fair_days = (result_fair_days?.value ?? []) as string[]

    const [initiated, setInitiated] = useState<boolean>(false)
    const [ticketTracker, setTicketTracker] = useState<LunchTicket[]>(tickets)
    const [shownTickets, setShownTickets] = useState<LunchTicket[]>(tickets)
    const [filterUsedState, setFilterUsedState] = useState<string>("All")
    const [filterDateState, setFilterDateState] = useState<string>("Any")

    // This should not be here... FIXUP LATER (move into redux state)
    useEffect(() => {
        if(!initiated && tickets.length > 0 && ticketTracker.length == 0){
            setInitiated(true);
            setTicketTracker(tickets);
        }

        //Filter tickets
        if (ticketTracker.length > 0) {
            const filteredTickets = ticketTracker.filter((ticket: LunchTicket) => {
                if (
                    filterUsedState == "All" ||
                    (ticket.used && filterUsedState == "Used") ||
                    (!ticket.used && filterUsedState == "Available")
                ) {
                    if (
                        filterDateState === "Any" ||
                        ticket.day.includes(filterDateState)
                    )
                        return ticket
                }
                return false
            })
            //update
            setShownTickets(filteredTickets as LunchTicket[])
        }else{
            setShownTickets([] as LunchTicket[])
        }
    }, [filterDateState, filterUsedState, tickets, ticketTracker, initiated])

    const deleteTicket = (lunchTicket:LunchTicket) => {
        const auxTickets = [...ticketTracker]
        auxTickets.splice(ticketTracker.indexOf(lunchTicket), 1);
        setTicketTracker([...auxTickets]);
        console.log(auxTickets)
    }

    return (
        <FormWrapper className="flex max-w-md flex-col gap-y-5 text-slate-700">
            <h2 className="text-md text-center font-bold">
                Here you can find all your lunch tickets
            </h2>
            <form className="w-lg flex">
                <div className="mr-auto w-1/3">
                    <label htmlFor="used-tickets" className="pr-2">
                        Ticket Status:
                    </label>
                    <Dropdown
                        value={filterUsedState}
                        onChange={event => {
                            setFilterUsedState(event.value)
                        }}
                        options={["All", "Available", "Used"]}
                        className="md:w-14rem w-full"
                    />
                </div>
                <div className="w-1/3">
                    <label htmlFor="ticket-date" className="pr-2">
                        Ticket date:
                    </label>
                    <Dropdown
                        value={filterDateState}
                        onChange={event => {
                            setFilterDateState(event.value)
                        }}
                        options={["Any", ...fair_days]}
                        className="md:w-14rem w-full"
                    />
                </div>
            </form>
            {shownTickets == null || shownTickets.length == 0 ? (
                <p className="pt-4 text-center font-semibold">
                    No tickets found under your company.
                </p>
            ) : (
                shownTickets.map((ticket, index) => (
                    <div key={index} className="+mb-6 min-w-75">
                        <LunchTicketView
                            key={index}
                            ticket={ticket}
                            deleteTicketFromList={deleteTicket}
                        ></LunchTicketView>
                    </div>
                ))
            )}
        </FormWrapper>
    )
}
