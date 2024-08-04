import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { useDashboard } from "@/shared/hooks/api/useDashboard"
import { HOST } from "@/shared/vars"
import { cn } from "@/utils/cx"
import { useMutation } from "@tanstack/react-query"
import { useParams } from "@tanstack/react-router"
import { HelpCircleIcon, Loader2Icon, Trash2Icon } from "lucide-react"
import { ReactNode, useState } from "react"
import { useDropzone } from "react-dropzone"
import { toast } from "sonner"
import { FormWrapper } from "../FormWrapper"

export function LogoFormPage() {
    const { companyId } = useParams({
        from: "/$companyId/*"
    })
    const { data } = useDashboard()
    const companyName = data?.company.name

    const defaultSquare = data?.exhibitor?.catalogue_logo_squared
    const defaultFreeSize = data?.exhibitor?.catalogue_logo_freesize

    const { mutate, isPending } = useMutation({
        mutationFn: async (data: { square: unknown; freeSize: unknown }) =>
            fetch(`${HOST}/api/dashboard/${companyId}`, {
                method: "PUT",
                body: JSON.stringify({
                    exhibitor: {
                        catalogue_logo_squared: data.square,
                        catalogue_logo_freesize: data.freeSize
                    }
                })
            }),
        onSuccess: async response => {
            if (response.status >= 200 && response.status < 300)
                toast.success("Invoice details updated")
            else {
                toast.error("Failed to update invoice details", {
                    description: JSON.stringify(await response.json())
                })
            }
        }
    })

    const [freeSizeImage, setFreeSizeImage] = useState<ArrayBuffer>()
    const [freeSizeFile, setFreeSizeFile] = useState<File>()
    const [squareImage, setSquareImage] = useState<ArrayBuffer>()
    const [squareFile, setSquareFile] = useState<File>()

    function convertBase64(file: File) {
        return new Promise((resolve, reject) => {
            const fileReader = new FileReader()
            fileReader.readAsDataURL(file)
            fileReader.onload = () => {
                resolve(fileReader.result)
            }
            fileReader.onerror = error => {
                reject(error)
            }
        })
    }

    async function onSubmitImage() {
        if (squareFile && freeSizeFile) {
            mutate({
                square: await convertBase64(squareFile),
                freeSize: await convertBase64(freeSizeFile)
            })
        } else if (squareFile) {
            mutate({
                square: await convertBase64(squareFile),
                freeSize: undefined
            })
        } else if (freeSizeFile) {
            mutate({
                square: undefined,
                freeSize: await convertBase64(freeSizeFile)
            })
        }
    }

    async function onClearLogos() {
        setSquareFile(undefined)
        setSquareImage(undefined)

        setFreeSizeFile(undefined)
        setFreeSizeImage(undefined)

        mutate({
            square: null,
            freeSize: null
        })
    }

    const squareImageURL =
        squareImage == null
            ? null
            : URL.createObjectURL(new Blob([squareImage]))
    const freeSizeImageURL =
        freeSizeImage == null
            ? null
            : URL.createObjectURL(new Blob([freeSizeImage]))

    return (
        <FormWrapper>
            <div className="flex flex-col items-center gap-10">
                <Alert className="max-w-md">
                    <HelpCircleIcon size={20} />
                    <AlertTitle>Tip!</AlertTitle>
                    <AlertDescription>
                        Visit{" "}
                        <a
                            className="text-emerald-500 underline"
                            href="https://armada.nu/student/exhibitors"
                        >
                            https://armada.nu/student/exhibitors
                        </a>{" "}
                        to get a grasp of how your logo will be displayed. (We
                        do not update this site in real-time)
                    </AlertDescription>
                </Alert>
                <div className="flex gap-2">
                    <Dropzone
                        image={squareImage}
                        setImage={setSquareImage}
                        file={squareFile}
                        setFile={setSquareFile}
                        text={
                            <p className="text-stone-400">
                                Drag and drop your{" "}
                                <span className="underline">square</span> logo
                                here
                            </p>
                        }
                    />
                    <Dropzone
                        image={freeSizeImage}
                        setImage={setFreeSizeImage}
                        file={freeSizeFile}
                        setFile={setFreeSizeFile}
                        text={
                            <p className="text-stone-400">
                                Drag and drop your logo here
                            </p>
                        }
                    />
                </div>

                <div className="rounded bg-orange-100 p-3">
                    <p className="text-orange-500">
                        File formats must be: (.png, .jpg or .gif)
                    </p>
                </div>
                {companyName && (
                    <div className="flex gap-x-4">
                        <Preview
                            title="Preview of your square logo"
                            companyName={companyName}
                            logo={squareImageURL || defaultSquare || ""}
                        />
                        <Preview
                            title="Preview of your free size logo"
                            companyName={companyName}
                            logo={freeSizeImageURL || defaultFreeSize || ""}
                        />
                    </div>
                )}
                <div className="flex gap-x-4">
                    <Button
                        type="submit"
                        className={cn("flex gap-4")}
                        onClick={onSubmitImage}
                    >
                        {isPending && <Loader2Icon className="animate-spin" />}{" "}
                        Submit and save
                    </Button>
                    <Button
                        className="gap-2"
                        variant={"destructive"}
                        onClick={onClearLogos}
                    >
                        <Trash2Icon size={20} />
                        Clear logos
                    </Button>
                </div>
            </div>
        </FormWrapper>
    )
}

function Dropzone({
    text,
    image,
    setImage,
    file,
    setFile
}: {
    text: ReactNode
    image?: ArrayBuffer
    setImage: (image: ArrayBuffer) => void
    file?: File
    setFile: (file: File) => void
}) {
    const { getRootProps, getInputProps } = useDropzone({
        onDrop: async acceptedFiles => {
            const file = acceptedFiles[0]
            if (file == null) {
                return
            }
            setFile(file)
            setImage(await file.arrayBuffer())
        },
        maxFiles: 1,
        accept: {
            "image/png": [".png"],
            "image/jpg": [".jpg", ".jpeg"],
            "image/gif": [".gif"]
        },
        maxSize: 2000000 // 2MB
    })

    const sizeFormatter = Intl.NumberFormat("en-US", {
        compactDisplay: "short",
        notation: "compact",
        maximumFractionDigits: 1
    })

    const imageURL =
        image == null ? null : URL.createObjectURL(new Blob([image]))

    return (
        <div
            {...getRootProps({ className: "dropzone" })}
            className="aspect-[4:3] flex min-h-[150px] w-full items-center justify-center rounded-lg border-2 border-dashed p-4 hover:cursor-pointer"
        >
            <input {...getInputProps()} />
            {imageURL ? (
                <div className="flex gap-x-4">
                    <div className="aspect-square max-w-[100px]">
                        <img
                            className="h-full w-full object-contain"
                            src={imageURL}
                            alt={"logo"}
                            width={300}
                            height={300}
                        />
                    </div>
                    <div className="flex flex-1 flex-col">
                        <p className="flex-nowrap whitespace-nowrap text-stone-600">
                            {file?.name}
                        </p>
                        <p className="lowercase text-stone-600">
                            {sizeFormatter.format(file?.size ?? 0)}b
                        </p>
                    </div>
                </div>
            ) : (
                text
            )}
        </div>
    )
}

function Preview({
    title,
    companyName,
    logo
}: {
    title: string
    companyName: string
    logo: string
}) {
    return (
        <div className="flex flex-col items-center">
            <h2 className="mb-4">{title}</h2>
            <>
                <div className="relative flex aspect-[4/3] w-60 flex-col rounded-lg border-2 border-solid border-emerald-900 bg-gradient-to-b from-emerald-900 via-emerald-950 to-stone-950">
                    <h3 className="xs:text-xl my-2 text-center text-2xl text-emerald-100 antialiased">
                        {companyName}
                    </h3>
                    <div className="relative mt-2 flex h-[70px] w-full flex-initial justify-center px-4">
                        <img
                            className="h-full w-full object-contain"
                            src={logo}
                            alt={companyName}
                            width={300}
                            height={300}
                        />
                    </div>
                </div>
            </>
        </div>
    )
}
