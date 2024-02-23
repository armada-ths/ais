import { HOST } from "../../shared/vars"

export async function sendTicket(
    ticketToken: string,
    setSendTicketError?: (msg: string) => void,
    setSendTicketStatus?: (msg: string) => void
) {
    try {
        const response = await fetch(
            `${HOST}/api/fair/lunchtickets/${ticketToken}/reactsend`
        )

        if (!response.ok) {
            try {
                const errorData = await response.json()
                if (errorData && errorData.message) {
                    setSendTicketError?.(
                        `Could not send ticket. Status: ${response.status}`
                    )
                } else {
                    setSendTicketError?.(
                        `Could not send ticket. Status: ${response.status}`
                    )
                }
            } catch (error) {
                console.error("Error parsing response:", error)
                setSendTicketError?.(
                    `Could not send ticket. Status: ${response.status}`
                )
            }
        } else {
            setSendTicketStatus?.("The ticket has been sent")
        }
    } catch (error) {
        setSendTicketError?.(
            "Could not send ticket. Internal Error: Contact the staff"
        )
    }
}
