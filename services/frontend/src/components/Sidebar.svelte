<script lang="ts">
    import {getContextClient, queryStore} from "@urql/svelte";
    import {GET_SHIP_FRAMES, GET_SHIP_NAME} from "../routes/queries";

    export let ship_id
    let ship

    $: {
        if (ship_id) {
            // console.log(ship_id)
            // noinspection TypeScriptValidateTypes
            ship = queryStore({
                client: getContextClient(),
                query: GET_SHIP_FRAMES,
                variables: {ship_id}
            });
            console.log($ship)
        }
    }
</script>

<div class="h-full text-center min-w-fit w-1/7 shadow-md bg-white inset-y-0 left-0" id="sidenav">
  <p>Frames</p>
  <ul class="relative px-1">
    <li class="relative">
      <span> 1st item </span>
    </li>
    <li class="relative">
      <span> 2nd item </span>
    </li>
  </ul>

</div>