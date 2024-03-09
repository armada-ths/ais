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

export async function queryRegistrationGroups() {
    const response = await fetch(`${HOST}/api/companies/registration_groups`)
    const data = (await response.json()) as RegistrationGroup[]
    return data
}

/**
 * These are groups that can be created in the AIS CRM,
 * used for things such as "interested in" and "registration groups"
 */
export function useRegistrationGroups() {
    return useQuery({
        queryKey: ["registration_groups"],
        queryFn: queryRegistrationGroups
    })
}
