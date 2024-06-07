export function formatCurrency(
    value?: number | null,
    options?: {
        fractionalDigits?: number
    }
) {
    if (value == null || isNaN(value)) {
        return "N/A"
    }
    return Intl.NumberFormat("sv").format(
        Math.round(value * 10 ** (options?.fractionalDigits ?? 0)) /
            10 ** (options?.fractionalDigits ?? 0)
    )
}
