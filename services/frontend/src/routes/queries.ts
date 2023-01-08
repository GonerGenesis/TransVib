import {gql} from "@urql/svelte";
export const GET_SHIP_NAME = gql`
    query GetShipData {
        getShip(id: 1){
            author {
                username
            }
            title
            id
        }
    }
`
export const GET_SHIP_FRAMES = gql`
    query GetShipData($ship_id: Int!) {
        getShip(id: $ship_id){
            frames {
                id
            }
        }
    }
`

export const GET_FRAME = gql`
    query GetFrameData($id: int) {
        getFrame(id: $id){
            framePoints {
                id
                y
                z
            }
            frameSegments {
                startPoint {
                    id
                }
                endPoint {
                    id
                }
            }
        }
    }
    `