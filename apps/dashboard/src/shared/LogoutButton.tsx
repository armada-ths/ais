import { HOST } from "@/shared/vars"

export function LogoutButton() {
    return (
        <a className="" href={`${HOST}/accounts/logout?next=/dashboard`}>
            <div className="m-4 mx-5 flex items-center gap-x-2 text-center text-slate-700 hover:text-slate-500">
                <p className="hover:underline">Sign Out</p>
                <span className="pi pi-sign-out" />
            </div>
        </a>
    )
}
