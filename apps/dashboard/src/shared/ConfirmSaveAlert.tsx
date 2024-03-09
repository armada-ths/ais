import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle
} from "@/components/ui/alert-dialog"
import { atom, createStore, useAtom } from "jotai"

// eslint-disable-next-line react-refresh/only-export-components
export const alertStore = createStore()

const confirmAlertOpen = atom(false)
const confirmAlertStatus = atom<"confirm" | "cancel" | null>(null)

// eslint-disable-next-line react-refresh/only-export-components
export function useConfirmSaveAlert() {
    const [, setOpen] = useAtom(confirmAlertOpen)
    const [, setStatus] = useAtom(confirmAlertStatus)
    return {
        confirm: async () => {
            setOpen(true)
            return new Promise<boolean>(resolve => {
                const unsub = alertStore.sub(confirmAlertStatus, () => {
                    unsub()
                    const status = alertStore.get(confirmAlertStatus)
                    setOpen(false)
                    setStatus(null)
                    resolve(status === "confirm")
                })
            })
        },
        cancel: () => {
            setOpen(false)
            setStatus(null)
        }
    }
}

export function ConfirmSaveAlert() {
    const [open, setOpen] = useAtom(confirmAlertOpen)
    const [, setStatus] = useAtom(confirmAlertStatus)
    return (
        <AlertDialog open={open} onOpenChange={setOpen}>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Unsaved changes</AlertDialogTitle>
                    <AlertDialogDescription>
                        You have not saved your changes on this page, are you
                        sure you want to proceed?
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel onClick={() => setStatus("cancel")}>
                        Cancel
                    </AlertDialogCancel>
                    <AlertDialogAction onClick={() => setStatus("confirm")}>
                        Continue
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    )
}
