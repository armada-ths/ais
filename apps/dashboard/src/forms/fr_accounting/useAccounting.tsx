import { Order } from "@/shared/hooks/api/useDashboard"
import { HOST } from "@/shared/vars"
import { useMutation } from "@tanstack/react-query"
import { toast } from "sonner"

export type OrderMutation = Pick<Order, "quantity"> & {
    product: Pick<Order["product"], "id">
}

function getOrderMutationData(orders: OrderMutation[]) {
    return orders.map(order => ({
        product: {
            id: order.product.id
        },
        quantity: order.quantity // Hard coded for now, sorry :(
    }))
}

export function useAccountingMutation(
    params?: Omit<
        Parameters<typeof useMutation>[0],
        "mutationFn" | "mutationKey"
    >
) {
    return useMutation({
        mutationKey: ["mutate_orders"],
        mutationFn: async (orders: OrderMutation[]) => {
            const response = fetch(`${HOST}/api/dashboard/`, {
                method: "PUT",
                body: JSON.stringify({
                    orders: getOrderMutationData(orders)
                })
            })
            return await (await response).json()
        },
        ...params,
        onSuccess: (data, variables, context) => {
            if ("error" in data) {
                if (params?.onError != null)
                    params.onError(data, variables, context)
                toast.error("Failed to save changes", {
                    description: `Something did not work trying to save your contact information. Please try again or contact us. Error: ${data.error}`
                })
                return
            }
            if (params?.onSuccess != null)
                return params?.onSuccess?.(data, variables, context)
            toast.success("Saved changes", {
                description: "Your contact information has been saved!"
            })
        },
        onError: (data, variables, context) => {
            if (params?.onError)
                return params?.onError?.(data, variables, context)
            toast.error("Failed to save changes", {
                description:
                    "Something did not work trying to save your contact information. Please try again or contact us."
            })
        }
    })
}
