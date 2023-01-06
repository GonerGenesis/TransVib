import {gql} from "@apollo/client";
export const GET_SHIP = gql`
    query GetShipData {
        getShip(id: 1){
            author {
                username
            }
            title
            frames {
                id
            }
        }
    }
`;

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