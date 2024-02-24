import { HOST } from "@/shared/vars"
import { useQuery } from "@tanstack/react-query"

export type RegistrationGroup = {
    id: number
    name: string
    children: Array<{
        id: number
        name: string
    }>
}

export function useRegistrationGroups() {
    return useQuery({
        queryKey: ["registration_groups"],
        queryFn: async () => {
            const response = await fetch(
                `${HOST}/api/companies/registration_groups`
            )
            return (await response.json()) as RegistrationGroup[]
        }
    })
}
