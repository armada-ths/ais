import { HOST } from "@/shared/vars"
import { useQuery } from "@tanstack/react-query"

export type CompaniesResponse = Array<{
    "Organization Name": string
    id: number
}>

export async function queryCompanies() {
    const response = await fetch(`${HOST}/api/companies`)
    const result = (await response.json()) as CompaniesResponse
    return result
}

export function useCompanies() {
    return useQuery({
        queryKey: ["companies"],
        queryFn: queryCompanies
    })
}
