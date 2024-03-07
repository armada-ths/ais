import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useRegistrationGroups } from "@/shared/hooks/api/useRegistrationGroups"
import { HOST } from "@/shared/vars"
import { queryClient } from "@/utils/query_client"
import { useMutation } from "@tanstack/react-query"
import { useEffect, useState } from "react"
import { toast } from "sonner"

export function IrInterestedInPage() {
    const { data } = useDashboard()
    const { data: registrationGroups } = useRegistrationGroups()

    const [groupPicks, setGroupPicks] = useState<{ id: number }[]>()

    useEffect(() => {
        setGroupPicks(data?.interested_in ?? [])
    }, [data?.interested_in])

    const { mutateAsync, isPending } = useMutation({
        mutationFn: async () => {
            return await fetch(`${HOST}/api/dashboard/`, {
                method: "PUT",
                body: JSON.stringify({
                    interested_in: groupPicks
                })
            })
        }
    })

    useEffect(() => {})

    async function toggleInterest(groupId: number) {
        const newInterestedIn = groupPicks?.slice() ?? []
        // Remove the group if it exists
        if (newInterestedIn?.find(x => x.id === groupId)) {
            newInterestedIn?.splice(
                newInterestedIn?.findIndex(x => x.id === groupId),
                1
            )
        } else {
            // Add the group if it doesn't exist
            newInterestedIn?.push({ id: groupId })
        }
        setGroupPicks(newInterestedIn)
    }

    async function saveChangesToRemote() {
        await mutateAsync()
        await queryClient.invalidateQueries({
            queryKey: ["dashboard"]
        })
        toast.success("Saved changes", {
            description: "Your interests have been saved!"
        })
    }

    return (
        <div className="flex flex-col gap-y-10">
            {registrationGroups?.map(group => (
                <div key={group.id}>
                    <h2 className="text-lg text-emerald-400">{group?.name}</h2>
                    {group.children.map(child => (
                        <div
                            key={child.id}
                            className="flex items-center gap-x-2"
                        >
                            <Checkbox
                                id={child.id.toString()}
                                checked={
                                    groupPicks?.find(x => x.id === child.id) !=
                                    null
                                }
                                onCheckedChange={() => toggleInterest(child.id)}
                            />
                            <label htmlFor={child.id.toString()}>
                                {child.name}
                            </label>
                        </div>
                    ))}
                </div>
            ))}
            <Button disabled={isPending} onClick={saveChangesToRemote}>
                Save information
            </Button>
        </div>
    )
}
