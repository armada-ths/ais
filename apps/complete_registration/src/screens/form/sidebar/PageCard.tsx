import { selectPageProgress } from "../../../store/form/form_selectors"
import { RootState } from "../../../store/store"
import { FormPage } from "../screen"
import { useSelector } from "react-redux"

export function PageCard({ page }: { page: FormPage }) {
    console.log(page.id)
    const progress = useSelector((state: RootState) =>
        selectPageProgress(state, page.id)
    )
    return (
        <div className="flex justify-between rounded bg-white p-2 px-4 shadow-sm">
            <h3 className="text-emerald-800">{page.title}</h3>
            {progress != null && (
                <p className="text-emerald-400">
                    {(progress * 100).toFixed(0)}%
                </p>
            )}
        </div>
    )
}
