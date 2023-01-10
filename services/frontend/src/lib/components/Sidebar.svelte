<script lang="ts">
    import {getContextClient, mutationStore, queryStore} from "@urql/svelte";
    import {GET_SHIP_FRAMES, GET_SHIP_NAME} from "$lib/gql_actions/queries.ts";
    import AddFramePopUp from "./AddFramePopUp.svelte";

    export let ship_id
    let ship
    let result

    let showModal = false
    function handleToggleModal(){
        showModal = !showModal
        //alert('clicked')
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
            // console.log($ship)
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
  <button on:click={handleToggleModal}
          class="inline-block px-6 py-2.5 bg-blue-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out">
    +
  </button>
  <AddFramePopUp
  title="Edit your details"
  open={showModal}
  on:close={handleToggleModal}
  >
  <!--<svelte:fragment slot="body">
    This is content inside my modal! 👋
  </svelte:fragment>-->
  </AddFramePopUp>


</div>