import { HOST } from "@/shared/vars"
import { useQuery } from "@tanstack/react-query"

export interface DatesResponse {
    fair: Fair
    ticket: Ticket
    ir: Ir
    fr: Fr
    events: {
        start: string // Date
        end: string // Date
    }
}

export interface Fair {
    description: string
    days: string[] // Dates
}

export interface Ticket {
    end: string // Date - after this date companies will no longer be able to modify their lunch or banquet tickets
}

export interface Ir {
    start: string // Date
    end: string // Date
    acceptance: string // Date - At this date companies will be informed if they got a spot at the fair
}

export interface Fr {
    start: string // Date
    end: string // Date
}

/**
 * Fetches relevant dates such as IR, FR etc...
 */
export async function fetchDates() {
    const response = await fetch(`${HOST}/api/dates`)
    const data = await response.json()
    return data as DatesResponse
}

export function useDates() {
    return useQuery({
        queryKey: ["dates"],
        queryFn: fetchDates
    })
}
