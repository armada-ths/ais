import React from "react"

export default function PrimarySection({
    children
}: {
    children: React.ReactNode
}) {
    return (
        <div className="flex flex-1 flex-col items-center border-x-[1px] border-solid border-l-slate-200 pt-5">
            {children}
        </div>
    )
}
