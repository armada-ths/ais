export const LogoutButton = () => {
	return <a className="p-3 " href="/accounts/logout?next=/register">
		<div className="my-5 flex items-center gap-x-2 text-center text-slate-700 hover:text-slate-500">
			<p className="underline">Sign Out</p>
			<span className="pi pi-sign-out" />
		</div>
	</a>
}