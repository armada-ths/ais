import { FormIds, FormPageIds } from "@/forms"
import { Form, FormPage } from "@/forms/form_types"
import { IfProgressDone } from "@/shared/IfProgressDone"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { useProducts } from "@/shared/hooks/api/useProducts"
import { remoteSaveChanges } from "@/store/form/async_actions"
import { AppDispatch } from "@/store/store"
import { useFormMeta } from "@/useFormMeta"
import { cx } from "@/utils/cx"
import { useNavigate } from "@tanstack/react-router"
import React from "react"
import { useDispatch } from "react-redux"

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
    selected,
    page,
    form
}: {
    selected: boolean
    page: FormPage
    form: Form
}) {
    const dispatch = useDispatch<AppDispatch>()
    const navigate = useNavigate({
        from: "/$companyId/form/$formKey/$formPageKey"
    })

    const { formPage } = useFormMeta()

    const { data: dataRegistration } = useDashboard()
    const { data: dataProducts } = useProducts()

    if (!dataRegistration || !dataProducts) return null

    const completed = page.isDone?.({
        form,
        products: dataProducts,
        dashboard: dataRegistration
    })

    function clickPageCard() {
        dispatch(remoteSaveChanges())
        navigate({
            to: "/$companyId/form/$formKey/$formPageKey",
            params: { formPageKey: page.id }
        })
    }

    return (
        <Card
            onClick={clickPageCard}
            className={cx(
                "flex-row items-center justify-between border-[1px] hover:cursor-pointer",
                {
                    "border-liqorice-700 border-opacity-50": selected,
                    "opacity-50": completed && page.id !== formPage?.id
                }
            )}
        >
            <div className="flex items-center gap-2">
                <IfProgressDone
                    page={
                        `${form.key}.${page?.id}` as `${FormIds}.${FormPageIds}`
                    }
                >
                    <span className="pi pi-check-circle text-emerald-400"></span>
                </IfProgressDone>
                <h3>{page.title}</h3>
            </div>
        </Card>
    )
}
