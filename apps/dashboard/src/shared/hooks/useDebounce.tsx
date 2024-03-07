import { useEffect, useRef, useState } from "react"

export function useDebounce<T>(
    value: T,
    callback: (value: T) => void,
    options?: {
        delay: number
    }
) {
    const timerRef = useRef<NodeJS.Timeout>()

    useEffect(() => {
        clearTimeout(timerRef.current)
        timerRef.current = setTimeout(
            () => callback(value),
            options?.delay ?? 200
        )
    }, [callback, options?.delay, value])
}

export function useDebounceValue<T>(
    value: T,
    options?: {
        delay: number
    }
) {
    const timerRef = useRef<NodeJS.Timeout>()
    const [debouncedValue, setDebouncedValue] = useState(value)

    useEffect(() => {
        clearTimeout(timerRef.current)
        timerRef.current = setTimeout(
            () => setDebouncedValue(value),
            options?.delay ?? 200
        )
    }, [options?.delay, value])

    return debouncedValue
}
