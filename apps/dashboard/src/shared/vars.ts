export const HOST = import.meta.env.DEV ? "http://localhost:3000" : ""
export const PACKAGE_KEY = "Package"
export const PACKAGE_NOT_VISIBLE_KEY = "Non Visible Package"

// ##########################
// @deprecated Please use RegistrationSection enum instead
export const EVENTS_REGISTRATION_SECTION_KEY = "Events"
export const EXTRAS_REGISTRATION_SECTION_KEY = "Extras"
export const PACKAGE_SECTION_KEY = "Packages"
// ###########################
export enum RegistrationSection {
    Events = "Events",
    Extras = "Extras",
    Packages = "Packages"
}
