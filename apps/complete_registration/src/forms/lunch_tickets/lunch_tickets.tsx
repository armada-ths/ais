import { useState } from "react"
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils"
import { Button } from "primereact/button"
import { HOST } from "../../shared/vars"

interface LunchTicketsProps {
    ticket: LunchTicket
    sendTicketUpdateList: (ticket: LunchTicket) => void
    deleteTicketFromList: (ticket: LunchTicket) => void
}

function LunchTicketView({
    ticket,
    sendTicketUpdateList,
    deleteTicketFromList
}: LunchTicketsProps) {
    const [moreInfoDisplayed, setMoreInfoDisplayed] = useState<boolean>(false)
    const [dietaryDisplayed, setDietaryDisplayed] = useState<boolean>(false)
    const [sendTicketError, setSendTicketError] = useState<string>("")
    const [sendTicketStatus, setSendTicketStatus] = useState<string>("")

    function dietaryButtonClickHandler() {
        setDietaryDisplayed(!dietaryDisplayed)
    }

    function moreInfoButtonClickHandler() {
        setMoreInfoDisplayed(!moreInfoDisplayed)
    }

    async function sendTicket() {
        try {
            const response = await fetch(
                `${HOST}/api/fair/lunchtickets/` + ticket.token + `/reactsend`
            )

            if (!response.ok) {
                try {
                    const errorData = await response.json()
                    if (errorData && errorData.message) {
                        setSendTicketError(
                            `Could not send ticket. Status: ${response.status}`
                        )
                    } else {
                        setSendTicketError(
                            `Could not send ticket. Status: ${response.status}`
                        )
                    }
                } catch (error) {
                    console.error("Error parsing response:", error)
                    setSendTicketError(
                        `Could not send ticket. Status: ${response.status}`
                    )
                }
            } else {
                setSendTicketStatus(
                    "The ticket has been sent to " + ticket.email_address
                )
                sendTicketUpdateList(ticket)
            }
        } catch (error) {
            setSendTicketError(
                "Could not send ticket. Internal Error: Contact the staff"
            )
        }
    }

    async function deleteTicket() {
        try {
            const response = await fetch(
                `${HOST}/api/fair/lunchtickets/` + ticket.token + `/reactremove`
            )

            if (!response.ok) {
                try {
                    const errorData = await response.json()
                    if (errorData && errorData.message) {
                        setSendTicketError(
                            `Could not send ticket. Status: ${response.status}`
                        )
                    } else {
                        setSendTicketError(
                            `Could not send ticket. Status: ${response.status}`
                        )
                    }
                } catch (error) {
                    console.error("Error parsing response:", error)
                    setSendTicketError(
                        `Could not send ticket. Status: ${response.status}`
                    )
                }
            } else {
                deleteTicketFromList(ticket)
            }
        } catch (error) {
            setSendTicketError(
                "Could not delete ticket. Internal Error: Contact the staff"
            )
        }
    }

    return (
        <div>
            {sendTicketError.length > 0 ? (
                <p className="text-red-500">{sendTicketError}</p>
            ) : (
                ""
            )}
            <div className="lunch-ticket border-2 border-b-0 border-solid">
                <div className="flex w-full pb-4 pl-4 pr-4 pt-2">
                    <p className="mb-5 grow text-xl font-bold">Lunch ticket</p>
                    <div className="grow text-right font-semibold">
                        <p>{ticket.day}</p>
                        <p>{ticket.time}</p>
                    </div>
                </div>
                <div className="flex pl-4">
                    <div
                        className={
                            "lunch-ticket-availability" +
                            (ticket.used ? " used" : "")
                        }
                    />
                    <p className="pl-2 font-semibold">
                        {ticket.used
                            ? "Used"
                            : ticket.sent
                            ? "Sent"
                            : "Assigned"}
                    </p>
                </div>
                <div className="more-info-container pt-2">
                    <button
                        className="cursor-pointer justify-center pb-2 pl-4"
                        onClick={moreInfoButtonClickHandler}
                    >
                        <span className="text-indigo-700 hover:underline">
                            {moreInfoDisplayed
                                ? "- See less details"
                                : "+ See more details"}
                        </span>
                    </button>
                    {moreInfoDisplayed ? (
                        <div className="more-info flex w-full flex-row border-t-2 px-4 pb-1 pt-2">
                            <div className="w-2/3 [&>*]:pb-2">
                                <div>
                                    <p className="font-semibold">Email:</p>
                                    <p>{ticket.email_address}</p>
                                </div>
                                {ticket.comment ? (
                                    <div>
                                        <p className="font-semibold">
                                            Comment:
                                        </p>
                                        <p>{ticket.comment}</p>
                                    </div>
                                ) : (
                                    ""
                                )}
                                {sendTicketStatus.length > 0 ? (
                                    <div>
                                        <p className="text-indigo-500">
                                            {sendTicketStatus}
                                        </p>
                                    </div>
                                ) : (
                                    ""
                                )}
                            </div>
                            <div className="[&>*]:bx-4 flex w-1/3 flex-row items-end justify-center gap-2 pb-2 [&>*]:h-8 [&>*]:w-1/2 [&>*]:border-none">
                                <Button
                                    style={{ padding: 0 }}
                                    className="lunch-ticket-button"
                                    label="Send"
                                    onClick={sendTicket}
                                />
                                <Button
                                    style={{ padding: 0 }}
                                    className="lunch-ticket-button"
                                    severity="danger"
                                    label="Delete"
                                    onClick={deleteTicket}
                                />
                            </div>
                        </div>
                    ) : (
                        ""
                    )}
                </div>
                <div className="dietary-restrictions-container">
                    {dietaryDisplayed ? (
                        <div>
                            <button
                                className="flex w-full cursor-pointer items-center justify-center border-b-2 border-t-2 bg-slate-100"
                                onClick={dietaryButtonClickHandler}
                            >
                                <span>Dietary Restrictions</span>
                                <img
                                    src="/static/images/chevron_down_icon.svg"
                                    className="rotate-180 px-2"
                                    alt="Chevron Down"
                                />
                            </button>
                            <div className="dietary-restrictions border-b-2">
                                {Object.entries(ticket.dietary_restrictions)
                                    .length > 0 ? (
                                    <div className="grid grid-cols-2 gap-4 pb-2 text-center [&>*]:pt-2">
                                        {Object.entries(
                                            ticket.dietary_restrictions
                                        ).map(restriction => {
                                            return (
                                                <p key={restriction[0]}>
                                                    {restriction[1]}
                                                </p>
                                            )
                                        })}
                                    </div>
                                ) : (
                                    ""
                                )}
                                {Object.keys(ticket.dietary_restrictions)
                                    .length > 0 &&
                                ticket.other_dietary_restrictions &&
                                ticket.other_dietary_restrictions.length > 0 ? (
                                    <div className="border-b-2" />
                                ) : (
                                    ""
                                )}
                                {ticket.other_dietary_restrictions &&
                                ticket.other_dietary_restrictions.length > 0 ? (
                                    <div className="py-2">
                                        <p className="px-4 text-left">
                                            <span className="font-semibold">
                                                Other dietary restrictions:{" "}
                                            </span>
                                            {ticket.other_dietary_restrictions}
                                        </p>
                                    </div>
                                ) : (
                                    ""
                                )}
                                {
                                    <p
                                        className="py-2 pl-4"
                                        style={{
                                            display:
                                                Object.entries(
                                                    ticket.dietary_restrictions
                                                ).length > 0 ||
                                                (ticket.other_dietary_restrictions &&
                                                    ticket
                                                        .other_dietary_restrictions
                                                        .length > 0)
                                                    ? "none"
                                                    : "block"
                                        }}
                                    >
                                        No dietary restrictions
                                    </p>
                                }
                            </div>
                        </div>
                    ) : (
                        <button
                            className="flex w-full cursor-pointer items-center justify-center border-b-2 border-t-2 bg-slate-100"
                            onClick={dietaryButtonClickHandler}
                        >
                            <span>Dietary Restrictions</span>
                            <img
                                src="/static/images/chevron_down_icon.svg"
                                className="px-2"
                                alt="Chevron Down"
                            />
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}

export default LunchTicketView
