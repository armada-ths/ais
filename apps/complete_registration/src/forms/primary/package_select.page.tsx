import { useSelector } from "react-redux"
import { FormField } from "../../screens/form/FormInput"
import { FormWrapper } from "../FormWrapper"
import { selectProductPackages } from "../../store/products/products_selectors"

export function PackageSelectFormPage() {
    const packages = useSelector(selectProductPackages)

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
