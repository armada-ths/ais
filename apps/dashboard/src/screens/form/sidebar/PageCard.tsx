import { FORMS } from "@/forms"
import { useProducts } from "@/shared/hooks/useProducts"
import { useDashboard } from "@/shared/hooks/useRegistration"
import React from "react"
import { useDispatch, useSelector } from "react-redux"
import { FormPage } from "../../../forms/form_types"
import { remoteSaveChanges } from "../../../store/form/async_actions"
import { selectActivePage } from "../../../store/form/form_selectors"
import { setPage } from "../../../store/form/form_slice"
import { AppDispatch } from "../../../store/store"
import { cx } from "../../../utils/cx"

type Props = React.HTMLAttributes<HTMLDivElement>

export function Card({ children, className, ...rest }: Props) {
    return (
        <div
            className={cx(
                "flex select-none flex-col rounded border-[0.5px] bg-white p-2 px-4 shadow-sm",
                className
            )}
            {...rest}
        >
            {children}
        </div>
    )
}

export function PageCard({
    page,
    form
}: {
    selected: boolean
    page: FormPage
    form: (typeof FORMS)[keyof typeof FORMS]
}) {
    const dispatch = useDispatch<AppDispatch>()
    const activePage = useSelector(selectActivePage)

    const { data: dataRegistration } = useDashboard()
    const { data: dataProducts } = useProducts()

    if (!dataRegistration || !dataProducts) return null

    const completed = page.isDone?.({
        form,
        products: dataProducts,
        registration: dataRegistration
    })

    function clickPageCard() {
        dispatch(remoteSaveChanges())
        dispatch(setPage(page.id))
    }

    return (
        <Card
            onClick={clickPageCard}
            className={cx(
                "flex-row items-center justify-between hover:cursor-pointer",
                completed && page.id !== activePage?.id && "opacity-50"
            )}
        >
            <div className="flex items-center gap-2">
                {completed && (
                    <span className="pi pi-check-circle text-emerald-400"></span>
                )}
                <h3>{page.title}</h3>
            </div>
        </Card>
    )
}
