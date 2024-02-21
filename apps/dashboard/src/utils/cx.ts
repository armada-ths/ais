import clsx, { ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
export function cx(...classes: ClassValue[]) {
    return twMerge(clsx(...classes))
}
export const cn = cx // alias for cx (used by shadcn)
