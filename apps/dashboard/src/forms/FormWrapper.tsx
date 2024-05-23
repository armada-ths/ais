import { ConfirmSaveAlert } from "@/shared/ConfirmSaveAlert"
import React from "react"
import { PrimaryFormHeader } from "./Header"

// eslint-disable-next-line react-refresh/only-export-components

export function FormWrapper({ children }: { children: React.ReactNode }) {
    return (
        <>
            <ConfirmSaveAlert />
            <PrimaryFormHeader />
            {children}
        </>
    )
}
