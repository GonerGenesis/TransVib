<script lang="ts">
    import {getContextClient, mutationStore, queryStore} from "@urql/svelte";
    import {GET_SHIP_FRAMES, GET_SHIP_NAME} from "../routes/queries";
    import {ADD_FRAME} from "../routes/mutations";

    export let ship_id
    let ship
    let result

    function addFrame({framePos, shipId}) {
        // noinspection TypeScriptValidateTypes
        result = mutationStore({
            client: getContextClient(),
            query: ADD_FRAME,
            variables: {framePos, shipId},
        })
        alert("add Frame")
        return result
    }

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
  <ol class="relative px-1">
    {#if $ship}
      {#if $ship.fetching}
        <li class="relative"> loading</li>
      {:else if $ship.error}
        <li class="relative"> ERROR: {$ship.error.message}</li>
      {:else}
        {#each $ship.data.getShip.frames as frame}
          <li class="relative"> {frame.framePos}</li>
        {/each}
      {/if}
    {/if}
  </ol>
  <button on:click={addFrame(ship_id)}
          class="inline-block px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out">
    +
  </button>

</div>