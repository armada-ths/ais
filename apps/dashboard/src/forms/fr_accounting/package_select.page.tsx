import { useSelector } from "react-redux"
import { FormField } from "../../screens/form/FormInput"
import { selectVisibleProductPackages } from "../../store/products/products_selectors"
import { FormWrapper } from "../FormWrapper"

export function PackageSelectFormPage() {
    const packages = useSelector(selectVisibleProductPackages)

    return (
        <FormWrapper>
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
