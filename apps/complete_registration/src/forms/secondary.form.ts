import { Form } from "../screens/form/screen"

export const form: Form = {
    name: "Mandatory info",
    description: "This is mandatory",
    pages: [
        {
            id: "primary_form",
            title: "Billing info",
            fields: [
                {
                    mapping: "company.orgname",
                    name: "orgName",
                    type: "input-text"
                },
                {
                    mapping: "company.country",
                    name: "Country code",
                    type: "input-text"
                },
                {
                    mapping: "company.accept",
                    name: "Do you accept the charges",
                    type: "input-switch"
                },
                {
                    mapping: "company.textarea",
                    name: "Describe your business",
                    type: "input-textarea"
                },
                {
                    mapping: "company.countr",
                    name: "How many employees do you have",
                    type: "input-select",
                    options: [
                        {
                            id: "1",
                            text: "HELLO"
                        },
                        {
                            id: "2",
                            text: "Second"
                        },
                        {
                            id: "3",
                            text: "Third"
                        }
                    ]
                },
                {
                    mapping: "company.dropdown",
                    name: "Cool dropdown",
                    type: "input-dropdown",
                    options: [
                        {
                            id: "1",
                            text: "First"
                        },
                        {
                            id: "2",
                            text: "Second"
                        },
                        {
                            id: "3",
                            text: "Third"
                        }
                    ]
                }
            ]
        },
        {
            id: "primary_form",
            title: "ANother page",
            fields: [
                {
                    mapping: "company.orgname",
                    name: "orgName",
                    type: "input-text"
                },
                {
                    mapping: "company.textarea",
                    name: "Describe your business",
                    type: "input-textarea"
                },
                {
                    mapping: "company.countr",
                    name: "How many employees do you have",
                    type: "input-select",
                    options: [
                        {
                            id: "1",
                            text: "HELLO"
                        },
                        {
                            id: "2",
                            text: "Second"
                        },
                        {
                            id: "3",
                            text: "Third"
                        }
                    ]
                },
                {
                    mapping: "company.dropdown",
                    name: "Cool dropdown",
                    type: "input-dropdown",
                    options: [
                        {
                            id: "1",
                            text: "First"
                        },
                        {
                            id: "2",
                            text: "Second"
                        },
                        {
                            id: "3",
                            text: "Third"
                        }
                    ]
                }
            ]
        }
    ]
}
