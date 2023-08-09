import React from "react"

export default function PrimarySection({
    children
}: {
    children: React.ReactNode
}) {
    return (
        <div className="mt-10 flex flex-1 flex-col items-center">
            {children}
        </div>
    )
}
