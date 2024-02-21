import { useQuery } from "@tanstack/react-query"
import { HOST } from "../vars"

export async function useLunchTickets(companyName: string) {
    return useQuery({
        queryKey: ["lunchtickets"],
        queryFn: async () => {
            const response = await fetch(
                `${HOST}/api/fair/lunchtickets/companysearch?company=${companyName}` // THIS SHOULD FETCH BY ID
            )
            return await response.json()
        }
    })
}
