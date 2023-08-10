import { useSelector } from "react-redux"
import { FormField } from "../../screens/form/FormInput"
import { FormWrapper } from "../FormWrapper"
import { selectProductPackages } from "../../store/products/products_selectors"

export function PackageSelectFormPage() {
    const packages = useSelector(selectProductPackages)
    console.log(packages)

    return (
        <FormWrapper>
            <div className="flex flex-wrap justify-center gap-5">
                {packages.map(productPackage => (
                    <FormField.Package
                        key={productPackage.id}
                        product={productPackage}
                        label=""
                        mapping=""
                    ></FormField.Package>
                ))}
            </div>
        </FormWrapper>
    )
}
