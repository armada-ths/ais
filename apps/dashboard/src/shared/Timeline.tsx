import { Badge } from "@/components/ui/badge"
import { RegistrationStatus } from "@/store/company/company_slice"
import { cx } from "@/utils/cx"

export interface TimelineStage {
    id: RegistrationStatus | RegistrationStatus[]
    title: string
    badgeText?: string
}

export function Timeline(
    props: {
        stages: TimelineStage[]
        current: RegistrationStatus
    } & React.HTMLProps<HTMLDivElement>
) {
    const { stages, current, className, ...rest } = props

    const currentIndex = stages.findIndex(stage =>
        Array.isArray(stage.id)
            ? stage.id.includes(current)
            : stage.id === current
    )
    const currentPercentage = currentIndex / (stages.length - 1)

    return (
        <div className={cx("flex h-16", className)} {...rest}>
            <div className="relative flex h-4 w-72 flex-1 justify-between rounded-3xl bg-stone-200">
                <div
                    style={{
                        width: `${currentPercentage * 100}%`
                    }}
                    className="absolute h-full rounded-3xl bg-emerald-400"
                />
                {stages.map((stage, index) => (
                    <div
                        key={
                            Array.isArray(stage.id)
                                ? stage.id.length <= 0
                                    ? index
                                    : stage.id.join("-")
                                : stage.id
                        }
                        className="relative"
                    >
                        <div
                            className={cx(
                                "aspect-square h-full scale-[1.7] rounded-full bg-emerald-400",
                                {
                                    "bg-stone-200": index > currentIndex
                                }
                            )}
                        ></div>
                        {stage.badgeText != null && (
                            <Badge
                                variant={"outline"}
                                className="absolute bottom-8 flex w-20 -translate-x-[40%] justify-center text-center text-sm font-normal text-stone-600"
                            >
                                {stage.badgeText}
                            </Badge>
                        )}
                        <p className="absolute mt-4 w-32 -translate-x-[40%] text-center text-sm text-stone-500">
                            {stage.title}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    )
}
