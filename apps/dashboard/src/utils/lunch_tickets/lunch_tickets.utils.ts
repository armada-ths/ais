export interface LunchTicket {
    id: number
    token: string
    sent: boolean
    company: string
    user: string
    email_address: string
    comment: string
    day: string
    time: string
    used: boolean
    dietary_restrictions: string[]
    other_dietary_restrictions: string
    url: string
}

export function validateLunchTicket(
    ticket: Partial<LunchTicket>,
    unassigned_lunch_tickets: number
) {
    if (unassigned_lunch_tickets < 1)
        throw new Error("Your company cannot create more lunch tickets")

    if (!ticket.company) throw new Error("Select a company")

    if (!ticket.email_address) throw new Error("Provide an email")
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

    if (!emailPattern.test(ticket.email_address))
        throw new Error("Invalid email")

    if (ticket.email_address.length > 255)
        throw new Error("Maximum email length is 255 characters")

    if (!ticket.day) throw new Error("Select a day")

    if (!ticket.time) throw new Error("Select a time")

    if (ticket.other_dietary_restrictions) {
        if (ticket.other_dietary_restrictions.length > 75)
            throw new Error(
                "Maximum 'other dietary restrictions' length is 75 characters"
            )
    }

    if (ticket.comment) {
        if (ticket.comment.length > 255)
            throw new Error("Maximum comment length is 255 characters")
    }
}
