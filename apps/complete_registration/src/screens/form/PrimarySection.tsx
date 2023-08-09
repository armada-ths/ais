import React from "react"

export default function PrimarySection({
	children
}: {
	children: React.ReactNode
}) {
	return <div className="flex justify-center">{children}</div>
}
