import { useState } from "react"
import { FormWrapper } from "../FormWrapper"
import { InputText } from "primereact/inputtext"
import { Dropdown } from "primereact/dropdown"
import { Checkbox } from "primereact/checkbox"
import { Button } from "primereact/button"
import { Badge } from "primereact/badge"
import {
    LunchTicket,
    validateLunchTicket
} from "../../utils/lunch_tickets/lunch_tickets.utils"
import { useDispatch, useSelector } from "react-redux"
import { selectCompanyName } from "../../store/company/company_selectors"
import { HOST } from "../../shared/vars"
import { RootState } from "../../store/store"
import { selectField } from "../../store/form/form_selectors"
import { toast } from "sonner"
import { setField, setPage } from "../../store/form/form_slice"
import { sendTicket } from "./send_ticket"

export function CreateLunchTicketsPage() {
    const dispatch = useDispatch()

    const resultUnassignedLunchTickets = useSelector((state: RootState) =>
        selectField(state, "unassigned_lunch_tickets")
    )
    const assignedLunchTickets = useSelector((state: RootState) =>
        selectField(state, "assigned_lunch_tickets")
    )?.value as LunchTicket[] | null
    const resultFairDays = useSelector((state: RootState) =>
        selectField(state, "fair_days")
    )
    const resultLunchTimes = useSelector((state: RootState) =>
        selectField(state, "lunch_times")
    )
    const allExistingDietaryRestrictions = (useSelector((state: RootState) =>
        selectField(state, "dietary_restrictions")
    )?.value ?? []) as string[]

    const unassignedLunchTickets = (resultUnassignedLunchTickets?.value ??
        []) as number
    const fairDays = (resultFairDays?.value ?? [""]) as string[]
    const lunchTimes = (resultLunchTimes?.value ?? [""]) as string[]

    const [DateState, setDateState] = useState<string>(fairDays[0])
    const [TimeState, setTimeState] = useState<string>(lunchTimes[0])
    const [selectableTimes, setSelectableTimes] = useState<string[]>(
        lunchTimes.filter(time => time.includes(DateState))
    )
    const [Email, setEmail] = useState<string>("")
    const [DietaryRestrictions, setDietaryRestrictions] = useState<string[]>([])
    const [OtherDietRestrictions, setOtherDietRestrictions] =
        useState<string>("")
    const [OtherComments, setOtherComments] = useState<string>("")
    const [ErrorString, setErrorString] = useState<string>("")

    const companyName = useSelector(selectCompanyName)

    function modifySelectableTimes(date: string) {
        const filteredTimes = lunchTimes.filter(time => time.includes(date))
        setSelectableTimes(filteredTimes)
        setTimeState(filteredTimes[0])
    }

    async function processForm(e: React.FormEvent<HTMLFormElement>) {
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
            validateLunchTicket(ticket, unassignedLunchTickets)
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error("Error:", error)
                const errorString = error.toString()
                setErrorString(errorString)
            }
        }

        try {
            const create_ticket_promise = fetch(
                `${HOST}/api/fair/lunchtickets/reactcreate`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(ticket)
                }
            )

            toast.promise(create_ticket_promise, {
                loading: "Creating ticket...",
                success: "Ticket created!",
                error: "Error creating ticket"
            })

            const response = await create_ticket_promise

            if (!response.ok) {
                try {
                    const errorData = await response.json()
                    if (errorData && errorData.message) {
                        setErrorString(errorData.message)
                    } else {
                        setErrorString("Unknown error")
                    }
                } catch (error) {
                    console.error("Error parsing response:", error)
                    setErrorString("Error parsing response")
                }
            } else {
                const data = await response.json()

                if (data.token == null) {
                    // Force browser to reload
                    window.location.reload()
                }
                // Send the ticket to the user's email
                sendTicket(data.token)
                // Add the ticket to state and mark it as sent
                dispatch(
                    setField({
                        mapping: "assigned_lunch_tickets",
                        value: [
                            ...(assignedLunchTickets ?? []),
                            {
                                ...ticket,
                                id: data.id,
                                token: data.token,
                                sent: true
                            } as LunchTicket
                        ]
                    })
                )
                dispatch(
                    setField({
                        mapping: "unassignedLunchTickets",
                        value: unassignedLunchTickets - 1
                    })
                )
                // Navigate back to the start view
                dispatch(setPage("view_ticket"))
            }
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
        } catch (error: any) {
            console.error("Error:", error)
            const errorString = error.toString()
            setErrorString(errorString)
        }
    }

    return (
        <FormWrapper className="flex flex-col gap-y-5 text-slate-700">
            <div className="mb-2 w-[450px] rounded bg-sky-100 p-2 px-4">
                <p className="text-sm text-sky-600">
                    Here you create your lunch tickets by specifying a timeslot
                    and dietary restictions. One lunch tickets corresponds to
                    one lunch, so for example 4 representatives both days will
                    need 8 lunch tickets. Reach out to your Host if you need to
                    buy more lunch tickets.
                </p>
            </div>
            <h2 className="text-md text-center font-bold">
                You can create
                {unassignedLunchTickets == 0 ? (
                    <Badge
                        value={unassignedLunchTickets.toString()}
                        severity="danger"
                        className="mx-2"
                    />
                ) : (
                    <Badge
                        value={unassignedLunchTickets.toString()}
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
                            modifySelectableTimes(event.value)
                        }}
                        options={fairDays}
                        className="w-full"
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
                        options={selectableTimes}
                        className="w-full"
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
                        {allExistingDietaryRestrictions.map(restriction => (
                            <div
                                key={restriction}
                                className="flex items-center gap-1"
                            >
                                <Checkbox
                                    key={restriction}
                                    checked={DietaryRestrictions.includes(
                                        restriction
                                    )}
                                    onChange={isChecked => {
                                        if (isChecked.checked) {
                                            setDietaryRestrictions(prev => [
                                                ...prev,
                                                restriction
                                            ])
                                        } else {
                                            setDietaryRestrictions(prev => [
                                                ...prev.filter(
                                                    name => name != restriction
                                                )
                                            ])
                                        }
                                    }}
                                />
                                {restriction}
                            </div>
                        ))}
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
                    <Button
                        label="Create lunch ticket"
                        disabled={unassignedLunchTickets == 0}
                    />
                </div>
            </form>
        </FormWrapper>
    )
}
