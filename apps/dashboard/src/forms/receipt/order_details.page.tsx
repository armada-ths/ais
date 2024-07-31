import { useEffect, useState } from "react"

import { Product } from "@/shared/hooks/api/useDashboard"
import { HOST } from "@/shared/vars"
import { cx } from "@/utils/cx"
import { formatCurrency } from "@/utils/format_currency"
import { FormWrapper } from "../FormWrapper"

type Order = {
    comment: string
    id: number
    quantity: number
    unit_price: number | null
    product: Product
}

const getOrderPrice = (order: Order) => {
    if (order.unit_price != null) {
        return order.unit_price
    }

    return order.product.unit_price * order.quantity
}

export const OrderDetails = () => {
    const [orders, setOrders] = useState<Order[] | undefined>()

    // Todo: Move to redux
    useEffect(() => {
        const update = async () => {
            fetch(`${HOST}/api/dashboard/`, {}).then(async raw => {
                const data = await raw.json()
                setOrders(data.orders)
            })
        }

        update()
    }, [setOrders])

    if (!orders) {
        return <>Loading</>
    }

    const totalPrice = orders.reduce(
        (acc, current) =>
            acc +
            (current.unit_price ??
                current.quantity * current.product.unit_price),
        0
    )
    const grossPrice = totalPrice * 1.25

    return (
        <FormWrapper>
            <div className={cx("flex flex-col gap-2")}>
                {orders.map(order => (
                    <div
                        key={order.id}
                        className={cx(
                            "flex select-none flex-col rounded border-[0.5px] bg-white p-2 px-4 shadow-sm"
                        )}
                    >
                        <p className="">
                            {order.product.short_name || order.product.name} x{" "}
                            {order.quantity}
                        </p>
                        {order.comment ? (
                            <p className="text-slate-400">{order.comment}</p>
                        ) : (
                            <></>
                        )}
                        <p className="mt-2 text-slate-400">
                            {formatCurrency(getOrderPrice(order))} kr
                        </p>
                    </div>
                ))}
            </div>
            <div className="mt-5 flex flex-col items-center justify-between rounded bg-slate-200 p-1 px-3">
                <div className="flex w-full justify-between">
                    <h2 className="text-lg">Net</h2>
                    <p className="text">{formatCurrency(totalPrice)} kr</p>
                </div>
                <div className="flex w-full justify-between">
                    <h2 className="text-lg">VAT</h2>
                    <p className="text">25%</p>
                </div>
                <div className="flex w-full justify-between">
                    <h2 className="text-lg">Gross</h2>
                    <p className="text font-bold">
                        {formatCurrency(grossPrice)} kr
                    </p>
                </div>
            </div>
        </FormWrapper>
    )
}
