export function formatCurrency(
    value: number,
    options?: {
        fractionalDigits?: number
    }
) {
    return Intl.NumberFormat("sv").format(
        Math.round(value * 10 ** (options?.fractionalDigits ?? 0)) /
            10 ** (options?.fractionalDigits ?? 0)
    )
}
