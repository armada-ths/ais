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

    return {
        cancel: () => clearTimeout(timerRef.current)
    }
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

export const debounce = <T extends (...args: unknown[]) => unknown>(
    callback: T,
    options?: {
        delay: number
    }
) => {
    let timeout: NodeJS.Timeout | null = null
    return (...args: Parameters<T>): ReturnType<T> => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        let result: any
        if (timeout) clearTimeout(timeout)
        timeout = setTimeout(
            () => {
                result = callback(...args)
            },
            options?.delay ?? 200
        )
        return result
    }
}
