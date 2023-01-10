import {getContextClient, mutationStore} from "@urql/svelte";
import {ADD_FRAME} from "$lib/gql_actions/mutations.ts";

/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({request}) => {
        const data = await request.formData();
        console.log(data)
    }
};


const addFrame = ({framePos, shipId}) => {
    // noinspection TypeScriptValidateTypes
    let result = mutationStore({
        client: getContextClient(),
        query: ADD_FRAME,
        variables: {framePos, shipId},
    })
}