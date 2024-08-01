import { DashboardResponse, Order } from "@/shared/hooks/api/useDashboard"
import { useOrders } from "@/shared/hooks/api/useOrders"
import { HOST } from "@/shared/vars"
import { useMutation } from "@tanstack/react-query"
import { useParams } from "@tanstack/react-router"
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
    TData extends DashboardResponse,
    TErr,
    TVar extends OrderMutation[]
>(
    params?: Omit<
        Parameters<typeof useMutation<TData, TErr, TVar>>[0],
        "mutationFn" | "mutationKey"
    >
) {
    const { companyId } = useParams({
        from: "/$companyId/*"
    })
    const { data: orders } = useOrders()

    const mutation = useMutation<TData, TErr, TVar>({
        mutationKey: ["mutate_orders"],
        mutationFn: async orders => {
            const response = await fetch(`${HOST}/api/dashboard/${companyId}`, {
                method: "PUT",
                body: JSON.stringify({
                    orders: getOrderMutationData(orders)
                })
            })
            return (await response.json()) as TData
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

    /**
     * Place product order
     * @param productId The id of the product you're picking
     * @param quantity How many instances of this product you want, 0 to remove it
     */
    async function setProductOrder(productId: number, quantity: number) {
        const newOrders = orders.filter(
            order => order.product.id !== productId
        ) as OrderMutation[] as TVar
        if (quantity > 0)
            newOrders.push({ product: { id: productId }, quantity })
        await mutation.mutateAsync(newOrders)
    }

    return {
        ...mutation,
        setProductOrder
    }
}
