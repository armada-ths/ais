import React from "react"

/**
 * Good for 404 screens and other info screens
 */
export function InfoScreen({
    children,
    title,
    subText
}: {
    children?: React.ReactNode
    title: string
    subText?: string
}) {
    return (
        <div className="flex h-screen w-screen flex-col justify-center">
            <div className="flex-1" />
            <div className="mx-auto flex max-w-[30rem] flex-[2] flex-col items-center">
                <h1 className="text-6xl font-bold text-emerald-400">{title}</h1>
                {subText && (
                    <h3 className="mt-5 text-lg text-emerald-900">{subText}</h3>
                )}
                {children}
            </div>
        </div>
    )
}
