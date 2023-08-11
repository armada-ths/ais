import { FORMS } from "../../forms"
import { cx } from "../../utils/cx"
import FormCard from "./FormCard"

export function DashboardScreen() {
    return (
        <div className={cx("grid min-h-[100dvh] grid-cols-[1fr_6fr_1fr]")}>
            <div>{/* SIDEBAR */}</div>
            <div className="flex flex-col items-center p-5">
                <div>
                    <h1 className="rounded bg-slate-400 p-2 px-8 text-4xl text-white">
                        Company AB
                    </h1>
                </div>
                <div className="mt-10 flex flex-wrap gap-5">
                    {Object.entries(FORMS)
                        /*                         .filter(current => current[0] === "primary") */
                        .map(([key, formMeta]) => (
                            <FormCard key={key} form={formMeta} />
                        ))}
                </div>
            </div>
            <div>{/* SIDEBAR */}</div>
        </div>
    )
}
