import React from "react"
import { cx } from "../utils/cx"

// Create attributes from html div
type Props = React.HTMLAttributes<HTMLDivElement>

export function FormWrapper({ className, children, ...rest }: Props) {
    return (
        <div className={cx("my-5", className)} {...rest}>
            {children}
        </div>
    )
}
