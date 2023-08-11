import { Card } from "../form/sidebar/PageCard"
import { FORMS } from "../../forms"

export default function FormCard({
    form
}: {
    form: (typeof FORMS)[keyof typeof FORMS]
}) {
    return (
        <Card key={form.key} className="max-w-sm p-5 px-8 text-slate-700">
            <p className="mb-2 text-lg">{form.name}</p>
            <p className="text-slate-500">
                {form.description}
                {form.description}
                {form.description}
                {form.description}
            </p>
        </Card>
    )
}
