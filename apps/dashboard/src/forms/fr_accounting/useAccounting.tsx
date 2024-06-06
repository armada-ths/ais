import { DashboardResponse, Order } from "@/shared/hooks/api/useDashboard"
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

export function useAccountingMutation<
    TRes extends DashboardResponse,
    TErr,
    TParam extends OrderMutation[]
>(
    params?: Omit<
        Parameters<typeof useMutation<TRes, TErr, TParam>>[0],
        "mutationFn" | "mutationKey"
    >
) {
    return useMutation({
        mutationKey: ["mutate_orders"],
        mutationFn: async orders => {
            const response = await fetch(`${HOST}/api/dashboard/`, {
                method: "PUT",
                body: JSON.stringify({
                    orders: getOrderMutationData(orders)
                })
            })
            return await response.json()
        },
        ...params,
        onSuccess: (data, variables, context) => {
            if ("error" in data) {
                if (params?.onError != null)
                    params.onError(data as TErr, variables, context)
                toast.error("Operation failed", {
                    description: `Something did not work trying to save your contact information. Please try again or contact us. Error: ${data.error}`
                })
                return
            }

            if (params?.onSuccess !== undefined)
                return params?.onSuccess?.(data, variables, context)
        },
        onError: (data, variables, context) => {
            if (params?.onError)
                return params?.onError?.(data, variables, context)
            toast.error("Operation failed", {
                description:
                    "Something did not work trying to save your contact information. Please try again or contact us."
            })
        }
    })
}
