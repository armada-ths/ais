import { useState } from "react"
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils"
import { Button } from "primereact/button"
import { HOST } from "../../shared/vars"
import { toast } from "sonner"
import { cx } from "../../utils/cx"
import { sendTicket } from "./send_ticket"
import { getCRSFToken } from "../../utils/django_format/django_format.utils"

interface LunchTicketsProps {
    ticket: LunchTicket
    sendTicketUpdateList: (ticket: LunchTicket) => void
    onRemoteDeleteSuccess: (ticket: LunchTicket) => void
}

function LunchTicketView({
    ticket,
    sendTicketUpdateList,
    onRemoteDeleteSuccess
}: LunchTicketsProps) {
    const [moreInfoDisplayed, setMoreInfoDisplayed] = useState<boolean>(false)
    const [dietaryDisplayed, setDietaryDisplayed] = useState<boolean>(false)
    const [deleteTicketError, setDeleteTicketError] = useState<string>("")
    const [deleteTicketStatus, setDeleteTicketStatus] = useState<string>("")

    function dietaryButtonClickHandler() {
        setDietaryDisplayed(!dietaryDisplayed)
    }

    function moreInfoButtonClickHandler() {
        setMoreInfoDisplayed(!moreInfoDisplayed)
    }

    async function deleteTicket() {
        try {
            const delete_ticket_promise = fetch(
                `${HOST}/api/fair/lunchtickets/${ticket.token}/reactremove`,{
                    headers: {
                        "Content-Type": "application/json",
                        'X-CSRFToken': getCRSFToken()
                    },
                    mode: 'same-origin',
                }
            )

            toast.promise(delete_ticket_promise, {
                loading: "Deleting ticket...",
                success: "Ticket deleted!",
                error: "Could not delete ticket"
            })

            const response = await delete_ticket_promise

            if (!response.ok) {
                try {
                    const errorData = await response.json()
                    if (errorData && errorData.message) {
                        setDeleteTicketError(
                            `Could not delete ticket. Status: ${response.status}`
                        )
                    } else {
                        setDeleteTicketError(
                            `Could not delete ticket. Status: ${response.status}`
                        )
                    }
                } catch (error) {
                    console.error("Error parsing response:", error)
                    setDeleteTicketError(
                        `Could not delete ticket. Status: ${response.status}`
                    )
                }
            } else {
                onRemoteDeleteSuccess(ticket)
            }
        } catch (error) {
            setDeleteTicketError(
                "Could not delete ticket. Internal Error: Contact the staff"
            )
        }
    }

    function triggerSend() {
        sendTicket(ticket.token, setDeleteTicketError, setDeleteTicketStatus)
        sendTicketUpdateList(ticket)
    }

    return (
        <div>
            {deleteTicketError.length > 0 ? (
                <p className="text-red-500">{deleteTicketError}</p>
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
                <div className="flex items-center pl-4">
                    <div
                        className={cx("h-2 w-2 rounded-full bg-yellow-400", {
                            "bg-red-400": ticket.used,
                            "bg-emerald-400": ticket.sent && !ticket.used
                        })}
                    />
                    <p className="pl-2 font-semibold">
                        {ticket.used
                            ? "Used"
                            : ticket.sent
                            ? `Sent to ${ticket.email_address}`
                            : "Created (not sent)"}
                    </p>
                </div>
                <div className="pl-4">
                {deleteTicketStatus.length > 0 ? (
                        <div>
                            <p className="text-indigo-500">
                                {deleteTicketStatus}
                            </p>
                        </div>
                    ) : (
                        ""
                )}
                </div>
                <div className="more-info-container pt-2">
                    <div className="flex items-center justify-between">
                        <button
                            className="cursor-pointer justify-center pl-4"
                            onClick={moreInfoButtonClickHandler}
                        >
                            <span className="text-indigo-700 hover:underline">
                                {moreInfoDisplayed
                                    ? "- See less details"
                                    : "+ See more details"}
                            </span>
                        </button>
                        <div className="my-2 mr-4 flex gap-2">
                            <Button
                                className="!p-2 !py-1"
                                label={ticket.sent ? "Resend" : "Send"}
                                onClick={triggerSend}
                            />
                            <Button
                                className="!p-2 !py-1"
                                severity="danger"
                                label="Delete"
                                onClick={deleteTicket}
                            />
                        </div>
                    </div>
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
                            </div>
                            <div className="[&>*]:bx-4 flex w-1/3 flex-row items-end justify-center gap-2 pb-2 [&>*]:h-8 [&>*]:w-1/2 [&>*]:border-none"></div>
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
                                        {Object.entries(ticket.dietary_restrictions).map((restriction) => <p key={restriction[0]}>{restriction[1]}</p>)}
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
