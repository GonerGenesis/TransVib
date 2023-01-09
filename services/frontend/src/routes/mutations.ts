import {gql} from "@urql/svelte";

export const ADD_FRAME = gql`
    mutation AddFrame($framePos: Float!, $shipId: Int!){
        createFrame(frame: {framePos: $framePos, shipId: $shipId}){
            id
            framePos
        }
    }`