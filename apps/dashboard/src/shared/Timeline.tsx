import { Badge } from "@/components/ui/badge"
import { cx } from "@/utils/cx"

export interface TimelineStage {
    id: unknown
    title: string
    badgeText?: string
}

export function Timeline(
    props: {
        stages: TimelineStage[]
        current: unknown
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
        <div className={cx("mt-10 flex h-16", className)} {...rest}>
            <div className="relative flex h-4 w-72 flex-1 justify-between rounded-3xl bg-stone-200">
                <div
                    style={{
                        width: `${currentPercentage * 100}%`
                    }}
                    className="absolute h-full rounded-3xl bg-emerald-400"
                />
                {stages.map((stage, index) => (
                    <div
                        // @ts-expect-error oupsis this broke when migrating from redux
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
                                variant={
                                    index <= currentIndex
                                        ? "outline"
                                        : "default"
                                }
                                className={cx(
                                    "absolute bottom-8 flex -translate-x-[40%] justify-center whitespace-nowrap text-center text-sm font-normal",
                                    {
                                        "bg-stone-200 text-stone-600 hover:bg-stone-200":
                                            index > currentIndex
                                    }
                                )}
                            >
                                {stage.badgeText}
                            </Badge>
                        )}
                        <p
                            className={cx(
                                "absolute mt-4 w-32 -translate-x-[40%] text-center text-sm text-stone-600",
                                {
                                    "text-stone-500 hover:text-stone-500":
                                        index > currentIndex
                                }
                            )}
                        >
                            {stage.title}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    )
}
