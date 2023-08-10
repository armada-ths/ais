import { useDispatch, useSelector } from "react-redux"
import { FormWrapper } from "../FormWrapper"
import {
    selectProductEvents,
    selectSelectedProduct
} from "../../store/products/products_selectors"
import {
    Product,
    pickProduct,
    unpickProduct
} from "../../store/products/products_slice"
import { InputText } from "primereact/inputtext"
import { RootState } from "../../store/store"
import { InputSwitch } from "primereact/inputswitch"

function EventInput({ product }: { product: Product }) {
    const dispatch = useDispatch()
    const selected = useSelector((state: RootState) =>
        selectSelectedProduct(state, product.id)
    )
    console.log("SELECTED", selected)

    function onChange(quantity: number) {
        if (quantity <= 0 || quantity == null) {
            dispatch(
                unpickProduct({
                    id: product.id
                })
            )
        } else {
            dispatch(
                pickProduct({
                    id: product.id,
                    quantity,
                    isPackage: false
                })
            )
        }
    }

    return (
        <div className="w-full rounded bg-white p-5 shadow-sm">
            <div className="flex justify-between gap-10">
                <div className="w-3/4">
                    <p className="text-xl">{product.name}</p>
                    <p className="text-sm">{product.description}</p>
                </div>
                <div className="flex items-center justify-center">
                    {product.max_quantity > 1 ? (
                        <InputSwitch
                            onChange={() => onChange(selected == null ? 1 : 0)}
                            checked={selected != null}
                        />
                    ) : (
                        <InputText
                            placeholder="Quantity"
                            className="w-40"
                            value={selected?.quantity.toString() ?? "0"}
                            min={0}
                            max={product.max_quantity}
                            type="number"
                            onChange={event =>
                                onChange(parseInt(event.target.value))
                            }
                        />
                    )}
                </div>
            </div>
        </div>
    )
}

export function EventsFormPage() {
    const events = useSelector(selectProductEvents)
    console.log("EVENTS", events)
    return (
        <FormWrapper>
            <div className="flex flex-col gap-5">
                {events.map(current => (
                    <EventInput key={current.id} product={current} />
                ))}
            </div>
        </FormWrapper>
    )
}
