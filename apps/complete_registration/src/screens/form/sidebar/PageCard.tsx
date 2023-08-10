import {
    selectActivePage,
    selectPageProgress
} from "../../../store/form/form_selectors"
import { setPage } from "../../../store/form/form_slice"
import { RootState } from "../../../store/store"
import { cx } from "../../../utils/cx"
import { FormPage } from "../screen"
import { useDispatch, useSelector } from "react-redux"

export function PageCard({
    selected,
    page
}: {
    selected: boolean
    page: FormPage
}) {
    const dispatch = useDispatch()
    const progress = useSelector((state: RootState) =>
        selectPageProgress(state, page.id)
    )
    const activePage = useSelector(selectActivePage)

    const completed = progress != null && progress >= 1

    function clickPageCard() {
        dispatch(setPage(page.id))
    }

    return (
        <div
            onClick={clickPageCard}
            className={cx(
                "flex select-none items-center justify-between rounded border-[0.5px] bg-white p-2 px-4 shadow-sm transition-all duration-100 hover:cursor-pointer active:scale-95",
                completed && page.id !== activePage.id && "opacity-70",
                selected && "border-2"
            )}
        >
            <div className="flex items-center gap-2">
                {completed && (
                    <span className="pi pi-check-circle text-emerald-400"></span>
                )}
                <h3 className="text-emerald-800">{page.title}</h3>
            </div>
            {progress != null && progress < 1 && (
                <p className="text-xs font-bold text-emerald-400">
                    {(progress * 100).toFixed(0)}%
                </p>
            )}
        </div>
    )
}
