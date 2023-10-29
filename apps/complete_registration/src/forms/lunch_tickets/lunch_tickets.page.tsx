import { useEffect, useState } from "react"
import { useSelector, useDispatch } from "react-redux"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { FormWrapper } from "../FormWrapper"
import { Dropdown } from "primereact/dropdown"
import LunchTicketView from "./lunch_tickets"
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils"
import { Button } from "primereact/button"
import { nextPage, setField } from "../../store/form/form_slice"
import "./lunch_ticket.css"

export function ViewLunchTicketsPage() {
    const dispatch = useDispatch()

    const result_tickets = useSelector((state: RootState) =>
        selectField(state, "assigned_lunch_tickets")
    )
    const result_fair_days = useSelector((state: RootState) =>
        selectField(state, "fair_days")
    )

    const result_unassigned_tickets = useSelector((state: RootState) =>
        selectField(state, "unassigned_lunch_tickets")
    )

    const tickets = (result_tickets?.value ?? []) as LunchTicket[]
    const fair_days = (result_fair_days?.value ?? []) as string[]
    const unassigned_tickets = (result_unassigned_tickets?.value ??
        -1) as number

    const [initiated, setInitiated] = useState<boolean>(false)
    const [ticketTracker, setTicketTracker] = useState<LunchTicket[]>(tickets)
    const [unassignedTicketsTracker, setUnassignedTicketsTracker] =
        useState<number>(unassigned_tickets)
    const [shownTickets, setShownTickets] = useState<LunchTicket[]>(tickets)
    const [filterUsedState, setFilterUsedState] = useState<string>("All")
    const [filterDateState, setFilterDateState] = useState<string>("Any")

    // This should not be here... FIXUP LATER (move into redux state)
    useEffect(() => {
        //Updates the useState variables once we get everything from Redux (Dind't find a better way to do this, if values placed directly on useState, the View never updates when receiving data from Redux)
        if (
            !initiated &&
            tickets.length > 0 &&
            ticketTracker.length == 0 &&
            unassigned_tickets > -1
        ) {
            setInitiated(true)
            setTicketTracker(tickets)
            setUnassignedTicketsTracker(unassigned_tickets)
        }

        //Filter tickets
        if (ticketTracker.length > 0) {
            const filteredTickets = ticketTracker.filter(
                (ticket: LunchTicket) => {
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
                }
            )
            //update
            setShownTickets(filteredTickets as LunchTicket[])
        } else {
            setShownTickets([] as LunchTicket[])
        }
    }, [
        filterDateState,
        filterUsedState,
        tickets,
        unassigned_tickets,
        ticketTracker,
        initiated,
        unassignedTicketsTracker
    ])

    function sendTicket(lunchTicket: LunchTicket) {
        const updatedTickets = ticketTracker.map(ticket => {
            // Check if the current ticket is the one you want to update
            if (ticket === lunchTicket) {
                // Create a new object with the updated 'sent' property
                return { ...ticket, sent: true }
            }
            // For other tickets, just return them as they are
            return ticket
        })

        // Update the state with the new array
        setTicketTracker(updatedTickets)
    }

    function removeTicketLocally(lunchTicket: LunchTicket) {
        //Delete lunchticket in view
        const auxTickets = [...ticketTracker]
        auxTickets.splice(ticketTracker.indexOf(lunchTicket), 1)

        //Update the View
        setTicketTracker([...auxTickets])
        setUnassignedTicketsTracker(unassignedTicketsTracker + 1)

        //Update in Redux
        dispatch(
            setField({
                mapping: "unassigned_lunch_tickets",
                value: unassignedTicketsTracker + 1
            })
        )
        dispatch(
            setField({
                mapping: "assigned_lunch_tickets",
                value: auxTickets
            })
        )
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
                <div />
            ) : (
                shownTickets.map((ticket, index) => (
                    <div key={ticket.token} className="+mb-6 min-w-75">
                        <LunchTicketView
                            key={index}
                            ticket={ticket}
                            sendTicketUpdateList={sendTicket}
                            onRemoteDeleteSuccess={removeTicketLocally}
                        />
                    </div>
                ))
            )}
            <Button
                label="Create Lunch Ticket"
                onClick={() => dispatch(nextPage())}
            />
        </FormWrapper>
    )
}
