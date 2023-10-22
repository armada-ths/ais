import { MouseEventHandler, useState } from "react";
import { LunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils";
import { Button } from 'primereact/button';

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

    const dietaryButtonClickHandler = () => {
        setDietaryDisplayed(!dietaryDisplayed);
    }

    const moreInfoButtonClickHandler = () => {
        setMoreInfoDisplayed(!moreInfoDisplayed);
    }

    return(
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
                            <p className="pl-2 font-semibold">{(ticket.used ? 'Used' : 'Assigned')}</p>
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
                                <div className="more-info flex flex-row w-full pb-1 border-t-2 pt-2">
                                    <div className="w-2/3 [&>*]:pb-2 [&>*]:pl-4">
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
                                    </div>
                                    <div className="flex flex-row w-1/3 px-2 pb-2 gap-2 justify-center items-end [&>*]:p-0 [&>*]:border-none [&>*]:w-1/2 [&>*]:h-8">
                                        <Button label="Send"/>
                                        <Button severity="danger" label="Delete" />
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
                                        <img src="/chevron_down_icon.svg" className="px-2 rotate-180" alt="Chevron Down" />
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
                                            <div className="w-full"><p className="text-left px-4"><span className="font-semibold">Other dietary restrictions: </span>{ticket.other_dietary_restrictions}</p></div>
                                            :
                                            ""
                                        )}
                                        {(<p className="pl-4" style={{ display: (Object.entries(ticket.dietary_restrictions).length > 0 || (ticket.other_dietary_restrictions && ticket.other_dietary_restrictions.length > 0) ? "none" : "block")}}>No dietary restrictions</p>)}
                                    </div>
                                </div>
                            :
                                <button className="w-full border-t-2 border-b-2 flex justify-center items-center cursor-pointer bg-slate-100" onClick={dietaryButtonClickHandler}>
                                    <span>Dietary Restrictions</span>
                                    <img src="/chevron_down_icon.svg" className="px-2" alt="Chevron Down" />
                                </button>
                            )}

                        </div>
                    </div>
    )
}

export default LunchTicketView;
