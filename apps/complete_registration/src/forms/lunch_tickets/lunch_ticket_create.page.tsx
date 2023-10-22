import { useState, useEffect } from "react";
import { FormWrapper } from "../FormWrapper"
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { LunchTicket, DietaryRestrictions, mapDietaryRestrictions, validateLunchTicket } from "../../utils/lunch_tickets/lunch_tickets.utils";
import { buildURLEncodedPayload } from "../../utils/django_format/django_format.utils";
import { useSelector } from "react-redux";
import {
    selectCompanyName
} from "../../store/company/company_selectors"
import './lunch_ticket.css';
import { HOST } from "../../shared/vars"

export function CreateLunchTicketsPage() {
    const initialDietaryRestrictions: DietaryRestrictions = {
        Apples: false,
        Avocado: false,
        Beef: false,
        Eggs: false,
        Fish: false,
        Gluten: false,
        Honey: false,
        Lactose: false,
        Leek: false,
        Legumes: false,
        Milk_protein: false,
        Nuts: false,
        Onion: false,
        Paprika: false,
        Peanuts: false,
        Pork: false,
        Soy: false,
        Tomatoes: false,
        Vegan: false,
        Vegetarian: false,
        Walnuts: false,
        Wheat: false
    };

    const [DateState, setDateState] = useState<string>("2023-11-21");
    const [TimeState, setTimeState] = useState<string>("11:00");
    const [Email, setEmail] = useState<string>("");
    const [DietaryRestrictions, setDietaryRestrictions] = useState<DietaryRestrictions>(initialDietaryRestrictions);
    const [OtherDietRestrictions, setOtherDietRestrictions] = useState<string>("");
    const [OtherComments, setOtherComments] = useState<string>("");
    const [ErrorString, setErrorString] = useState<string>("");

    useEffect(() => {}, [DietaryRestrictions]);
    const companyName = useSelector(selectCompanyName);

    const processForm = async(e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const ticket : Partial<LunchTicket> = {
            company: companyName,
            email_address: Email,
            comment: OtherComments,
            day: DateState,
            time: TimeState,
            dietary_restrictions: mapDietaryRestrictions(DietaryRestrictions),
            other_dietary_restrictions: OtherDietRestrictions,
        }

        try{
            validateLunchTicket(ticket);
        }catch (error: unknown) {
            if (error instanceof Error) {
                console.error("Error:", error);
                const errorString = error.toString();
                setErrorString(errorString);
                return;
            }
        }

        try{
            await fetch((`${HOST}/api/fair/lunchtickets/reactcreate`), {method: "POST", headers: {"Content-Type": "application/x-www-form-urlencoded"}, body: buildURLEncodedPayload(ticket),})
            .then(async (response) => {
                //Return error
              if (!response.ok) {
                const errorData = await response.json();
                setErrorString(errorData.error);
              }else
                console.log('OK');
            })
            .catch((error) => {
                //Return error
                console.error("Error:", error);
                const errorString = error.toString();
                setErrorString(errorString);
            });
        }catch(error){
            console.error("Error:", error);
        }
    }

    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <h2 className="font-bold text-md text-center">Here you can create your lunch tickets</h2>
            <form className="flex flex-col [&>label]:font-bold [&>label]:pt-4 [&>div]:mb-4" onSubmit={processForm}>
                <p className="text-red-500">{ErrorString}</p>
                <div>
                    <label htmlFor="ticket-date" className="pr-2 font-bold">Day:*</label>
                    <Dropdown required={true} value={DateState} onChange={(event) => {
                            setDateState(event.value);
                        }} options={['2023-11-21', '2023-11-22']} className="w-full md:w-14rem" />
                </div>
                <div>
                    <label htmlFor="ticket-date" className="pr-2 block font-bold">Timeslot:*</label>
                    <Dropdown required={true} value={TimeState} onChange={(event) => {
                            setTimeState(event.value);
                        }} options={['11:00', '11:30', '12:00', '12:30', '13:00', '13:30']} className="w-full md:w-14rem" />
                </div>
                <div className="[&>*]:w-full">
                    <label htmlFor="user-email" className="pr-2 font-bold">Email:*</label>
                    <InputText required={true} value={Email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div>
                    <label htmlFor="dietary-restrictions" className="pr-2 font-bold">Dietary restrictions:</label>
                    <div id="dietary-restrictions-list" className="grid grid-cols-2 [&>div]:pt-2">
                            {
                                Object.entries(DietaryRestrictions).map(([restriction, value]) => {
                                    return(
                                        <div key={restriction}>
                                            <Checkbox
                                                key={restriction}
                                                checked={value}
                                                onChange={(isChecked) =>{
                                                    setDietaryRestrictions((prev) => ({
                                                        ...prev,
                                                        [restriction]: isChecked.checked,
                                                    }))
                                                }}
                                            />
                                            {restriction}
                                        </div>
                                    );
                                })
                            }
                    </div>
                </div>
                <div className="[&>*]:w-full">
                    <label htmlFor="other-dietary-restrictions" className="pr-2 block font-bold">Other dietary restrictions</label>
                    <InputText value={OtherDietRestrictions} onChange={(e) => setOtherDietRestrictions(e.target.value)} />
                </div>
                <div className="[&>*]:w-full">
                    <label htmlFor="other-comments" className="pr-2 block font-bold">Other comments</label>
                    <InputText value={OtherComments} onChange={(e) => setOtherComments(e.target.value)} />
                </div>
                <div className="mt-2 w-1/2 [&>*]:w-full [&>*]:py-1 m-auto">
                    <Button label="Create lunch ticket" />
                </div>

            </form>
        </FormWrapper>
    )
}
