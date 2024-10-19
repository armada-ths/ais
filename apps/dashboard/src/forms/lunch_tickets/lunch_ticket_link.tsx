import { Button } from "@/components/ui/button"
import { FormWrapper } from "../FormWrapper"

export function LunchTicketLink() {
    return (
        <FormWrapper>
            <div className="h-full w-full items-center justify-center text-center">
                <a href="https://forms.gle/q32AX9viPDx2SnCu9 ">
                    <Button>Go to lunch ticket form</Button>
                </a>
                <div className="mt-10">
                    <p>
                        If your company does not allow google forms, you can
                        email:{" "}
                    </p>
                    <p>
                        <a
                            className="font-bold"
                            href="mailto:service@armada.nu"
                        >
                            service@armada.nu
                        </a>
                    </p>
                </div>
            </div>
        </FormWrapper>
    )
}
