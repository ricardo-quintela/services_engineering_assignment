/**
 * Gets the current state of the document's cookies
 * @returns an object containing the names and values of the current state of the cookies
 */
export function getCookies() {
    return document.cookie
        .trim()
        .split(";")
        .map((value) => value.trim().split("="))
        .reduce((accumulator, value) => {
            accumulator[value[0]] = value[1];
            return accumulator;
        }, {} as { [name: string]: string });
}

/**
 * Sets a cookie in the document
 * @param name the name of the cookie
 * @param value the value of the cookie
 */
export function setCookie(name: string, value: string) {
    document.cookie = `${name}=${value}; `;
}

/**
 * Removes a cookie in the document
 * @param name the name of the cookie
 */
export function removeCookie(name: string) {
    const cookies = getCookies();

    document.cookie = "";

    console.log(Object.keys(cookies)
        .filter((key) => key !== name));
        // .forEach((key) => {
        //     document.cookie = `${name}=${cookies[key]}; `;
        // });
}
