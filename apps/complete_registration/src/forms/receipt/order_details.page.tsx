import { useEffect, useState } from "react"

import { HOST } from "../../shared/vars"
import { cx } from "../../utils/cx"
import { Product } from "../../store/products/products_slice"
import { FormWrapper } from "../FormWrapper"

type Order = {
	comment: string,
	id: number,
	quantity: number,
	unit_price: number | null,
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
			fetch(`${HOST}/api/registration/`, {}).then(async raw => {
				const data = await raw.json();
				setOrders(data.orders)
			})
		}

		update()
	}, [setOrders])

	if (!orders) {
		return <>Loading</>
	}

	return (
		<FormWrapper>
			<div className={cx("flex flex-col gap-2")}>
				{orders.map((order) =>
					<div
						key={order.id}
						className={cx(
							"flex select-none flex-col rounded border-[0.5px] bg-white p-2 px-4 shadow-sm"
						)}
					>
						<p className="">{order.product.name} x {order.quantity}</p>
						{
							order.comment ? <p className="text-slate-400">{order.comment}</p> : <></>
						}
						<p className="mt-2 text-slate-400">
							{Intl.NumberFormat("sv").format(getOrderPrice(order))} kr
						</p>
					</div>)}
			</div>
		</FormWrapper>
	)
}
