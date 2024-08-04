import { Label } from "@/components/ui/label"
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger
} from "@/components/ui/tooltip"
import { cn } from "@/utils/cx"
import { InfoIcon } from "lucide-react"

export function InputLabel({
    children,
    htmlFor,
    required,
    tooltip
}: {
    children: React.ReactNode
    htmlFor: string
    required?: boolean
    tooltip?: string
}) {
    return (
        <div className="flex justify-between py-1">
            <Label
                htmlFor={htmlFor}
                className={cn("flex items-center gap-2", {
                    "font-thin": !required
                })}
            >
                {children}
                {!required && <p className="text-xs">(optional)</p>}
            </Label>
            {tooltip != null && (
                <Tooltip>
                    <TooltipTrigger type="button">
                        <InfoIcon size={15} />
                    </TooltipTrigger>
                    <TooltipContent>
                        <p className="text-sm">{tooltip}</p>
                    </TooltipContent>
                </Tooltip>
            )}
        </div>
    )
}

export function InputErrorMessageText({ message }: { message: string }) {
    return <p className="text-xs text-red-500">{message}</p>
}
