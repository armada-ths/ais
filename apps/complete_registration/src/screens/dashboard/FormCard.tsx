import { Card } from "../form/sidebar/PageCard"
import { FORMS } from "../../forms"

export default function FormCard({
    formMeta
}: {
    formMeta: (typeof FORMS)[keyof typeof FORMS]
}) {
    return (
        <Card
            key={formMeta.form.key}
            className="max-w-sm p-5 px-8 text-slate-700"
        >
            <p className="mb-2 text-lg">{formMeta.form.name}</p>
            <p className="text-slate-500">
                {formMeta.form.description}
                {formMeta.form.description}
                {formMeta.form.description}
                {formMeta.form.description}
            </p>
        </Card>
    )
}
