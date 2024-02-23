import { useSelector } from "react-redux"
import { FormField } from "../../screens/form/FormInput"
import { FormWrapper } from "../FormWrapper"
import { selectVisibleProductPackages } from "../../store/products/products_selectors"

export function PackageSelectFormPage() {
    const packages = useSelector(selectVisibleProductPackages)

    return (
        <FormWrapper className="max-w-none">
            <div className="flex flex-wrap justify-center gap-5">
                {packages.map(productPackageMeta => (
                    <FormField.Package
                        key={productPackageMeta.id}
                        product={productPackageMeta}
                        label=""
                        mapping=""
                    />
                ))}
            </div>
        </FormWrapper>
    )
}
