import { useSelector } from "react-redux"
import { FormField } from "../../screens/form/FormInput"
import { FormWrapper } from "../FormWrapper"
import { selectProductPackages } from "../../store/products/products_selectors"
import { PrimaryFormHeader } from "./Header"

export function PackageSelectFormPage() {
    const packages = useSelector(selectProductPackages)
    console.log("PACKAGES", packages)

    return (
        <FormWrapper>
            <PrimaryFormHeader />
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
