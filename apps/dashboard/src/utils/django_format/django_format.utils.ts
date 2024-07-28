export function getCRSFToken() {
    const name = "csrftoken"
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1, cookie.length)
        }
    }
    throw new Error("Cookie not found")
}

export function ObjectToURLEncoded(object: object): string {
    const mapping = Object.keys(object)
        .map(key => {
            const objectKey = key as keyof object
            if (!objectKey) return
            if (Array.isArray(object[objectKey])) {
                const objectArray: Array<string | number | boolean> =
                    object[objectKey]
                let result = ""
                for (let i = 0; i < objectArray.length; i++) {
                    if (result != "") result += "&"
                    result += objectKey + "=" + objectArray[i]
                }
                return result
            }
            if (typeof object[objectKey] === "object")
                return ObjectToURLEncoded(object[objectKey])
            else {
                return objectKey + "=" + object[objectKey]
            }
        })
        .join("&")

    return mapping
}

export function buildURLEncodedPayload(data: object) {
    const token = getCRSFToken()
    return "crsfmiddlewaretoken=" + token + "&" + ObjectToURLEncoded(data)
}
