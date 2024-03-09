import { selectField } from "@/store/form/form_selectors"
import { setField, setPage } from "@/store/form/form_slice"
import { RootState } from "@/store/store"
import { LunchTicket } from "@/utils/lunch_tickets/lunch_tickets.utils"
import { Button } from "primereact/button"
import { Dropdown } from "primereact/dropdown"
import { useMemo, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { FormWrapper } from "../FormWrapper"
import "./lunch_ticket.css"
import LunchTicketView from "./lunch_tickets"

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

    // eslint-disable-next-line react-hooks/exhaustive-deps
    const tickets = (result_tickets?.value ?? []) as LunchTicket[]
    const fair_days = (result_fair_days?.value ?? []) as string[]
    const unassigned_tickets = (result_unassigned_tickets?.value ??
        -1) as number

    const [ticketTracker, setTicketTracker] = useState<LunchTicket[]>(tickets)
    const [unassignedTicketsTracker, setUnassignedTicketsTracker] =
        useState<number>(unassigned_tickets)
    const [filterUsedState, setFilterUsedState] = useState<string>("All")
    const [filterDateState, setFilterDateState] = useState<string>("Any")

    const shownTickets = useMemo(() => {
        return tickets.filter((ticket: LunchTicket) => {
            if (
                filterUsedState == "All" ||
                (ticket.used && filterUsedState == "Used") ||
                (!ticket.used && filterUsedState == "Available")
            ) {
                if (
                    filterDateState === "Any" ||
                    ticket.day.includes(filterDateState)
                )
                    return true
            }
            return false
        })
    }, [filterDateState, filterUsedState, tickets])

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
                    <div key={ticket.id} className="+mb-6 min-w-75">
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
                onClick={() => dispatch(setPage("create_ticket"))}
            />
        </FormWrapper>
    )
}
