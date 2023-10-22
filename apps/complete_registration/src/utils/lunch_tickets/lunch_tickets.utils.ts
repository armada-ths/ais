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

export function validateLunchTicket(ticket: Partial<LunchTicket>){
    if(!ticket.company)
        throw new Error("Select a company");

    if(!ticket.email_address)
        throw new Error("Provide an email");
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!emailPattern.test(ticket.email_address))
        throw new Error("Invalid email");

    if(ticket.email_address.length > 255)
        throw new Error("Maximum email length is 255 characters");

    if(!ticket.day)
        throw new Error("Select a day");

    if(!ticket.time)
        throw new Error("Select a time");

    if(ticket.other_dietary_restrictions){
        if(ticket.other_dietary_restrictions.length > 75)
            throw new Error("Maximum 'other dietary restrictions' length is 75 characters");
    }

    if(ticket.comment){
        if(ticket.comment.length > 255)
            throw new Error("Maximum comment length is 255 characters");
    }

}
