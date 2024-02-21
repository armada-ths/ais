export function PrimaryFormHeader() {
    return (
        <div className="flex w-full justify-center">
            <div className="mb-10 w-[450px] rounded bg-slate-200 p-2 px-4">
                <p className="text-slate-600">
                    Contact your sales representative or reach out on{" "}
                    <a
                        className="underline"
                        href="mailto:customer.support@armada.nu"
                    >
                        customer.support@armada.nu
                    </a>{" "}
                    if you have any questions.
                </p>
            </div>
        </div>
    )
}
