import React from "react"
import {
    selectActivePage,
    selectFormPageProgress
} from "../../../store/form/form_selectors"
import { setPage } from "../../../store/form/form_slice"
import { AppDispatch, RootState } from "../../../store/store"
import { cx } from "../../../utils/cx"
import { useDispatch, useSelector } from "react-redux"
import { remoteSaveChanges } from "../../../store/form/async_actions"
import { FormPage } from "../../../forms/form_types"

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

export function PageCard({ page }: { selected: boolean; page: FormPage }) {
    const dispatch = useDispatch<AppDispatch>()
    const calcProgress = useSelector((state: RootState) =>
        selectFormPageProgress(state, page.id)
    )
    const customProgress = useSelector(page.getProgress ?? (() => null))
    const progress = customProgress != null ? customProgress : calcProgress
    const activePage = useSelector(selectActivePage)

    const completed = progress != null && progress >= 1

    function clickPageCard() {
        dispatch(remoteSaveChanges())
        dispatch(setPage(page.id))
    }

    return (
        <Card
            onClick={clickPageCard}
            className={cx(
                "flex-row items-center justify-between hover:cursor-pointer",
                completed && page.id !== activePage?.id && "opacity-70"
            )}
        >
            <div className="flex items-center gap-2">
                {completed && (
                    <span className="pi pi-check-circle text-emerald-400"></span>
                )}
                <h3 className="text-emerald-800">{page.title}</h3>
            </div>
            {progress != null && progress < 1 && progress > 0 && (
                <p className="text-xs font-bold text-emerald-400">
                    {(progress * 100).toFixed(0)}%
                </p>
            )}
        </Card>
    )
}
