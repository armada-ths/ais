import { useState } from "react";
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils";
import { Button } from 'primereact/button';
import { HOST } from "../../shared/vars"

interface LunchTicketsProps{
    ticket:LunchTicket;
}

const LunchTicketView: React.FC<LunchTicketsProps> = (
    {
        ticket
    }
) => {
    const [moreInfoDisplayed, setMoreInfoDisplayed] = useState<boolean>(false);
    const [dietaryDisplayed, setDietaryDisplayed] = useState<boolean>(false);
    const [sendTicketError, setSendTicketError] =useState<string>("");
    const [sendTicketStatus, setSendTicketStatus] =useState<string>("");

    const dietaryButtonClickHandler = () => {
        setDietaryDisplayed(!dietaryDisplayed);
    }

    const moreInfoButtonClickHandler = () => {
        setMoreInfoDisplayed(!moreInfoDisplayed);
    }

    const sendTicket = async () => {
        try {
            const response = await fetch(`${HOST}/api/fair/lunchtickets/`+ticket.token+`/reactsend`);

            if (!response.ok) {
                setSendTicketError(`Could not send ticket. Status: ${response.status}`);
            }else{
                setSendTicketStatus("The ticket has been sent to "+ticket.email_address);
            }

            } catch (error) {
                setSendTicketError("Could not send ticket. Internal Error: Contact the staff");
            }
    }

    const deleteTicket = async () => {
        try {
            const response = await fetch(`${HOST}/api/fair/lunchtickets/`+ticket.token+`/reactremove`);

            if (!response.ok) {
                setSendTicketError(`Could not delete ticket. Status: ${response.status}`);
            }

            } catch (error) {
                setSendTicketError("Could not delete ticket. Internal Error: Contact the staff");
            }
    }

    return(
        <div>
        {(sendTicketError.length > 0 ? <p className="text-red-500">{sendTicketError}</p> : "")}
        <div className="lunch-ticket border-solid border-2 border-b-0">
                        <div className="flex w-full pt-2 pb-4 pl-4 pr-4">
                            <p className="text-xl mb-5 grow font-bold">Lunch ticket</p>
                            <div className="text-right grow font-semibold">
                                <p>{ticket.day}</p>
                                <p>{ticket.time}</p>
                            </div>
                        </div>
                        <div className="flex pl-4">
                            <div className={"lunch-ticket-availability" + ((ticket.used ? " used" : ""))} />
                            <p className="pl-2 font-semibold">{(ticket.used ? 'Used' : (ticket.sent ? 'Sent' : 'Assigned'))}</p>
                        </div>
                        <div className="more-info-container pt-2">
                            <button className="justify-center cursor-pointer pb-2 pl-4" onClick={moreInfoButtonClickHandler}>
                                <span className="hover:underline text-indigo-700">
                                {(moreInfoDisplayed ?
                                    "- See less details"
                                :
                                    "+ See more details"
                                )}
                                </span>
                            </button>
                            {(moreInfoDisplayed ?
                                <div className="more-info flex flex-row w-full pb-1 border-t-2 pt-2 px-4">
                                    <div className="w-2/3 [&>*]:pb-2">
                                        <div>
                                            <p className="font-semibold">Email:</p>
                                            <p>{ticket.email_address}</p>
                                        </div>
                                        {(ticket.comment ?
                                            <div>
                                                <p className="font-semibold">Comment:</p>
                                                <p>{ticket.comment}</p>
                                            </div>
                                            :
                                            ""
                                        )}
                                        {(sendTicketStatus.length > 0 ? <div><p className="text-indigo-500">{sendTicketStatus}</p></div> : "")}
                                    </div>
                                    <div className="flex flex-row w-1/3 pb-2 gap-2 justify-center items-end [&>*]:bx-4 [&>*]:border-none [&>*]:w-1/2 [&>*]:h-8">
                                        <Button style={{ padding: 0 }} className="lunch-ticket-button" label="Send" onClick={sendTicket}/>
                                        <Button style={{ padding: 0 }} className="lunch-ticket-button" severity="danger" label="Delete" onClick={deleteTicket}/>
                                    </div>
                                </div>
                            :
                            ""
                            )}
                        </div>
                        <div className="dietary-restrictions-container">
                            {(dietaryDisplayed ?
                                <div>
                                    <button className="w-full border-t-2 border-b-2 flex justify-center items-center cursor-pointer bg-slate-100" onClick={dietaryButtonClickHandler}>
                                        <span>Dietary Restrictions</span>
                                        <img src="/static/images/chevron_down_icon.svg" className="px-2 rotate-180" alt="Chevron Down" />
                                    </button>
                                    <div className="dietary-restrictions border-b-2">
                                        {(Object.entries(ticket.dietary_restrictions).length > 0 ?
                                        <div className="grid grid-cols-2 gap-4 text-center [&>*]:pt-2 pb-2">
                                            {Object.entries(ticket.dietary_restrictions).map((restriction) => {
                                                return <p key={restriction[0]}>{restriction[1]}</p>;
                                            })}
                                        </div>
                                        :
                                        ""
                                        )}
                                        {(ticket.dietary_restrictions.length>0 && (ticket.other_dietary_restrictions && ticket.other_dietary_restrictions.length > 0) ?
                                        <div className="border-b-2"/>
                                        :
                                        ""
                                        )}
                                        {(ticket.other_dietary_restrictions && ticket.other_dietary_restrictions.length > 0 ?
                                            <div className="py-2"><p className="text-left px-4"><span className="font-semibold">Other dietary restrictions: </span>{ticket.other_dietary_restrictions}</p></div>
                                            :
                                            ""
                                        )}
                                        {(<p className="pl-4 py-2" style={{ display: (Object.entries(ticket.dietary_restrictions).length > 0 || (ticket.other_dietary_restrictions && ticket.other_dietary_restrictions.length > 0) ? "none" : "block")}}>No dietary restrictions</p>)}
                                    </div>
                                </div>
                            :
                                <button className="w-full border-t-2 border-b-2 flex justify-center items-center cursor-pointer bg-slate-100" onClick={dietaryButtonClickHandler}>
                                    <span>Dietary Restrictions</span>
                                    <img src="/static/images/chevron_down_icon.svg" className="px-2" alt="Chevron Down" />
                                </button>
                            )}

                        </div>
                    </div>
                </div>
    )
}

export default LunchTicketView;
