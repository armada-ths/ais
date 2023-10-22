import { MouseEventHandler } from "react";
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils";

interface LunchTicketsProps{
    ticket:LunchTicket;
    displayDietaryRestrictions: MouseEventHandler<HTMLButtonElement>;
}

const LunchTicketView: React.FC<LunchTicketsProps> = (
    {
        ticket,
        displayDietaryRestrictions,
    }
) => {
    return(
        <div className="lunch-ticket border-solid border-2 border-b-0">
                        <div className="flex w-full pt-2 pb-4 pl-4 pr-4">
                            <p className="text-xl mb-5 grow font-bold">Lunch ticket</p>
                            <div className="text-right grow font-semibold">
                                <p>{ticket.day}</p>
                                <p>{ticket.time}</p>
                            </div>
                        </div>
                        <div className="flex pl-4 pb-1">
                            <div className={"lunch-ticket-availability" + ((ticket.used ? " used" : ""))} />
                            <p className="pl-2 font-semibold">{(ticket.used ? 'Used' : 'Assigned')}</p>
                        </div>
                        <div className="pl-4 pb-1">
                            <p><span className="font-semibold">Email:</span> {ticket.email_address}</p>
                            {(ticket.comment ?
                                <p><span className="font-semibold">Comment:</span> {ticket.comment}</p>
                                :
                                ""
                            )}
                        </div>
                        <div className="dietary-restrictions-container">
                            <button className="w-full border-t-2 border-b-2 flex justify-center cursor-pointer" onClick={displayDietaryRestrictions}>
                                <span>Dietary Restrictions</span>
                                <img src="/chevron_down_icon.svg" className="pl-2" alt="Chevron Down" />
                            </button>
                            <div className="dietary-restrictions border-b-2" style={{display: 'none'}}>
                                <div className="grid grid-cols-2 gap-4 text-center [&>*]:pt-2 pb-2">
                                    {Object.entries(ticket.dietary_restrictions).map((restriction) => {
                                        return <p key={restriction[0]}>{restriction[1]}</p>;
                                    })}
                                    <p style={{ display: (Object.entries(ticket.dietary_restrictions).length > 0 || (ticket.other_dietary_restrictions && ticket.other_dietary_restrictions.length > 0) ? "none" : "block")}}>No dietary restrictions</p>
                                </div>
                                {(ticket.other_dietary_restrictions && ticket.other_dietary_restrictions.length > 0 ?
                                    <div className="w-full"><p className="text-left px-4"><span className="font-semibold">Other dietary restrictions: </span>{ticket.other_dietary_restrictions}</p></div>
                                    :
                                    ""
                                )}
                            </div>
                        </div>
                    </div>
    )
}

export default LunchTicketView;
