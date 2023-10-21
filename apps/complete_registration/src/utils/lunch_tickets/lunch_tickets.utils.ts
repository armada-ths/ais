export enum DietaryRestrictionsEnum{
    Vegan = 1,
    Vegetarian,
    Peanuts,
    Milk_protein,
    Eggs,
    Wheat,
    Soy,
    Fish,
    Pork,
    Lactose,
    Leek,
    Apples,
    Tomatoes,
    Beef,
    Onion,
    Paprika,
    Nuts,
    Honey,
    Walnuts,
    Avocado,
    Gluten,
    Legumes
}

export interface DietaryRestrictions{
    Apples:boolean,
    Avocado:boolean,
    Beef:boolean,
    Eggs:boolean,
    Fish:boolean,
    Gluten:boolean,
    Honey:boolean,
    Lactose:boolean,
    Leek:boolean,
    Legumes:boolean,
    Milk_protein:boolean,
    Nuts:boolean,
    Onion:boolean,
    Paprika:boolean,
    Peanuts:boolean,
    Pork:boolean,
    Soy:boolean,
    Tomatoes:boolean,
    Vegan:boolean,
    Vegetarian:boolean,
    Walnuts:boolean,
    Wheat:boolean
}

export interface LunchTicket{
    company: string;
    user: string;
    email_address: string;
    comment: string;
    day: string;
    time: string;
    used: boolean;
    dietary_restrictions: [];
    other_dietary_restrictions: string;
}

export function mapDietaryRestrictions(dietaryRestrictions:DietaryRestrictions) : []{
    return Object.keys(dietaryRestrictions).map((key) => {
        if(dietaryRestrictions[key as keyof DietaryRestrictions]){
            return DietaryRestrictionsEnum[key as keyof typeof DietaryRestrictionsEnum];
        }
    }).filter((value) => value !== undefined) as [];
}
