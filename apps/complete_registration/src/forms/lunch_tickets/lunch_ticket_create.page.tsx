import { useState, useEffect } from "react"
import { FormWrapper } from "../FormWrapper"
import { InputText } from "primereact/inputtext"
import { Dropdown } from "primereact/dropdown"
import { Checkbox } from "primereact/checkbox"
import { Button } from "primereact/button"
import { Badge  } from "primereact/badge"
import {LunchTicket, validateLunchTicket} from "../../utils/lunch_tickets/lunch_tickets.utils"
import { buildURLEncodedPayload } from "../../utils/django_format/django_format.utils"
import { useSelector } from "react-redux"
import { selectCompanyName } from "../../store/company/company_selectors"
import "./lunch_ticket.css"
import { HOST } from "../../shared/vars"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"

export function CreateLunchTicketsPage() {
    const result_unassigned_lunch_tickets = useSelector((state: RootState) =>
        selectField(state, "unassigned_lunch_tickets")
    );
    const result_fair_days = useSelector((state: RootState) =>
        selectField(state, "fair_days")
    );
    const result_lunch_times = useSelector((state: RootState) =>
        selectField(state, "lunch_times")
    );
    const result_dietary_restrictions = useSelector((state: RootState) =>
        selectField(state, "dietary_restrictions")
    );

    const unassigned_lunch_tickets = (result_unassigned_lunch_tickets?.value ?? []) as number
    const fair_days = (result_fair_days?.value ?? [""]) as string[]
    const lunch_times = (result_lunch_times?.value ?? [""]) as string[]
    const dietary_restrictions = (result_dietary_restrictions?.value ?? []) as string[]

    const initialDietaryRestrictions: { [key: string]: boolean } = {};

    dietary_restrictions.forEach(name => {
        initialDietaryRestrictions[name] = false;
    });


    const [DateState, setDateState] = useState<string>(fair_days[0])
    const [TimeState, setTimeState] = useState<string>(lunch_times[0])
    const [Email, setEmail] = useState<string>("")
    const [DietaryRestrictions, setDietaryRestrictions] =
        useState<{ [key: string]: boolean }>(initialDietaryRestrictions)
    const [OtherDietRestrictions, setOtherDietRestrictions] =
        useState<string>("")
    const [OtherComments, setOtherComments] = useState<string>("")
    const [ErrorString, setErrorString] = useState<string>("")

    useEffect(() => {}, [DietaryRestrictions])
    const companyName = useSelector(selectCompanyName)

    const processForm = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        const ticket: Partial<LunchTicket> = {
            company: companyName,
            email_address: Email,
            comment: OtherComments,
            day: DateState,
            time: TimeState,
            dietary_restrictions: DietaryRestrictions,
            other_dietary_restrictions: OtherDietRestrictions
        }

        try {
            validateLunchTicket(ticket, unassigned_lunch_tickets)
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error("Error:", error)
                const errorString = error.toString()
                setErrorString(errorString)
                return
            }
        }

        try {
            await fetch(`${HOST}/api/fair/lunchtickets/reactcreate`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: buildURLEncodedPayload(ticket)
            })
                .then(async response => {
                    //Return error
                    if (!response.ok) {
                        const errorData = await response.json()
                        setErrorString(errorData.error)
                    } else{
                        //Reload: Not best practice, but I need to retrieve the token of the recently created ticket and place it on the queue
                        window.location.reload();
                    }
                })
                .catch(error => {
                    //Return error
                    console.error("Error:", error)
                    const errorString = error.toString()
                    setErrorString(errorString)
                })
        } catch (error) {
            console.error("Error:", error)
        }
    }

    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <h2 className="text-md text-center font-bold">
                You can create
                {(unassigned_lunch_tickets==0 ?
                <Badge
                    value={unassigned_lunch_tickets.toString()}
                    severity="danger"
                    className="mx-2"
                />
                :
                <Badge
                    value={unassigned_lunch_tickets.toString()}
                    className="mx-2"
                />
                )}
                lunch tickets
            </h2>
            <form
                className="flex flex-col [&>div]:mb-4 [&>label]:pt-4 [&>label]:font-bold"
                onSubmit={processForm}
            >
                <p className="text-red-500">{ErrorString}</p>
                <div>
                    <label htmlFor="ticket-date" className="pr-2 font-bold">
                        Day:*
                    </label>
                    <Dropdown
                        required={true}
                        value={DateState}
                        onChange={event => {
                            setDateState(event.value)
                        }}
                        options={fair_days}
                        className="md:w-14rem w-full"
                    />
                </div>
                <div>
                    <label
                        htmlFor="ticket-date"
                        className="block pr-2 font-bold"
                    >
                        Timeslot:*
                    </label>
                    <Dropdown
                        required={true}
                        value={TimeState}
                        onChange={event => {
                            setTimeState(event.value)
                        }}
                        options={lunch_times}
                        className="md:w-14rem w-full"
                    />
                </div>
                <div className="[&>*]:w-full">
                    <label htmlFor="user-email" className="pr-2 font-bold">
                        Email:*
                    </label>
                    <InputText
                        required={true}
                        value={Email}
                        onChange={e => setEmail(e.target.value)}
                    />
                </div>
                <div>
                    <label
                        htmlFor="dietary-restrictions"
                        className="pr-2 font-bold"
                    >
                        Dietary restrictions:
                    </label>
                    <div
                        id="dietary-restrictions-list"
                        className="grid grid-cols-2 [&>div]:pt-2"
                    >
                        {Object.entries(DietaryRestrictions).map(
                            ([restriction, value]) => {
                                return (
                                    <div key={restriction}>
                                        <Checkbox
                                            key={restriction}
                                            checked={value}
                                            onChange={isChecked => {
                                                setDietaryRestrictions(prev => ({
                                                    ...prev,
                                                    [restriction]: isChecked.checked
                                                  }) as { [key: string]: boolean });
                                            }}
                                        />
                                        {restriction}
                                    </div>
                                )
                            }
                        )}
                    </div>
                </div>
                <div className="[&>*]:w-full">
                    <label
                        htmlFor="other-dietary-restrictions"
                        className="block pr-2 font-bold"
                    >
                        Other dietary restrictions
                    </label>
                    <InputText
                        value={OtherDietRestrictions}
                        onChange={e => setOtherDietRestrictions(e.target.value)}
                    />
                </div>
                <div className="[&>*]:w-full">
                    <label
                        htmlFor="other-comments"
                        className="block pr-2 font-bold"
                    >
                        Other comments
                    </label>
                    <InputText
                        value={OtherComments}
                        onChange={e => setOtherComments(e.target.value)}
                    />
                </div>
                <div className="m-auto mt-2 w-1/2 [&>*]:w-full [&>*]:py-1">
                    {(unassigned_lunch_tickets==0 ?
                    <Button label="Create lunch ticket" disabled/>
                    :
                    <Button label="Create lunch ticket" />
                    )}
                </div>
            </form>
        </FormWrapper>
    )
}
