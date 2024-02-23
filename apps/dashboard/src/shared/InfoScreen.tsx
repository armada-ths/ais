import { Link, LinkComponent, useParams } from "@tanstack/react-router"
import React from "react"
import { cx } from "../utils/cx"

/**
 * Good for 404 screens and other info screens
 */
export function InfoScreen({
    children,
    title,
    subText,
    link,
    fullscreen,
    severity
}: {
    children?: React.ReactNode
    title: string
    link?: {
        text?: string
        to?: Parameters<LinkComponent>[0]["to"]
    } | null
    subText?: string
    fullscreen?: boolean
    severity?: "error" | "warning" | "info"
}) {
    const { companyId } = useParams()
    return (
        <div
            className={cx(
                "mx-10 flex flex-col justify-center",
                fullscreen !== false && "h-screen w-screen"
            )}
        >
            {fullscreen !== false && <div className="flex-1" />}
            <div className="mx-auto flex max-w-[30rem] flex-[2.5] flex-col items-center">
                <h1
                    className={cx("text-6xl font-bold text-emerald-400", {
                        "text-red-400": severity === "error",
                        "text-yellow-400": severity === "warning"
                    })}
                >
                    {title}
                </h1>
                {subText && (
                    <h3 className="mt-5 text-lg text-emerald-900">{subText}</h3>
                )}
                {link !== null && (
                    <Link
                        className="mt-5 underline "
                        // eslint-disable-next-line @typescript-eslint/no-explicit-any
                        to={
                            (link?.to ??
                                `/${companyId != null ? companyId : ""}`) as any
                        }
                    >
                        {link?.text ?? "Return to dashboard"}
                    </Link>
                )}
                {children}
            </div>
        </div>
    )
}
