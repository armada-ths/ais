import { useEffect, useState } from "react"

import { Form } from "../../screens/form/screen"
import { HOST } from "../../shared/vars"
import { InvoiceDetailsFormPage } from "../primary/invoice_details.page"
import { Product } from "../../store/products/products_slice"
import { cx } from "../../utils/cx"
import { PrimaryFormHeader } from "../primary/Header"

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

const OrderDetails = () => {
    const [orders, setOrders] = useState<Order[] | undefined>()

    useEffect(() => {
        const update = async () => {
            fetch(`${HOST}/api/registration/`, {}).then(async raw => {
                const data = await raw.json();
                setOrders(data.orders)
            })
        }

        update()
    }, [setOrders])

    console.log(orders)

    if (!orders) {
        return <>Loading</>
    }

    return (
        <>
            <PrimaryFormHeader />
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
        </>
    )
}

export const form: Form = {
    key: "receipt",
    name: "Order & Invoice Details",
    description:
        "On this page you select products and entry of company invoice details. Once submitted, no changes are permitted.",
    isSkippable: false,
    pages: [
        {
            id: "details",
            title: "Order details",
            hasNextButton: false,
            hasPrevButton: false,
            getProgress(_) {
                return 100
            },
            pageComponent: OrderDetails
        },
        {
            id: "invoice",
            title: "Invoice Information",
            hasNextButton: false,
            hasPrevButton: false,
            getProgress(_) {
                return 100
            },
            pageComponent: () => <InvoiceDetailsFormPage readOnly={true} />,
            fields: [
                {
                    mapping: "company.invoice_name"
                },
                {
                    mapping: "company.invoice_email_address"
                },
                {
                    mapping: "company.identity_number"
                },
                {
                    mapping: "company.invoice_address_line_1"
                },
                {
                    mapping: "company.invoice_address_line_2",
                    mandatory: false
                },
                {
                    mapping: "company.invoice_address_line_3",
                    mandatory: false
                },
                {
                    mapping: "company.invoice_zip_code"
                },
                {
                    mapping: "company.invoice_city"
                },
                {
                    mapping: "company.invoice_country"
                },
                {
                    mapping: "company.invoice_reference"
                }
            ]
        },
    ]
}
