import { configureStore } from "@reduxjs/toolkit"
import formReducer from "./form/form_slice"
import productsReducer from "./products/products_slice"
import companyReducer from "./company/company_slice"

export const store = configureStore({
    devTools: import.meta.env.DEV,
    reducer: {
        formMeta: formReducer,
        products: productsReducer,
        company: companyReducer
    },
    middleware(getDefaultMiddleware) {
        return getDefaultMiddleware({
            serializableCheck: false
        })
    }
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch
