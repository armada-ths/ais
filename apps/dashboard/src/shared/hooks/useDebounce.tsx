import { useEffect, useRef, useState } from "react"

export function useDebounce<T>(
    value: T,
    callback: (value: T) => void,
    options?: {
        delay?: number
    }
) {
    const initialized = useRef(false)
    const timerRef = useRef<NodeJS.Timeout>()

    useEffect(() => {
        if (!initialized.current) {
            initialized.current = true
            return
        }
        clearTimeout(timerRef.current)
        timerRef.current = setTimeout(
            () => callback(value),
            options?.delay ?? 200
        )
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [value])
}

export function useDebounceValue<T>(
    value: T,
    options?: {
        delay?: number
    }
) {
    const initialized = useRef(false)
    const timerRef = useRef<NodeJS.Timeout>()
    const [debouncedValue, setDebouncedValue] = useState(value)

    useEffect(() => {
        if (!initialized.current) {
            initialized.current = true
            return
        }
        clearTimeout(timerRef.current)
        timerRef.current = setTimeout(
            () => setDebouncedValue(value),
            options?.delay ?? 200
        )
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [value])

    return debouncedValue
}
