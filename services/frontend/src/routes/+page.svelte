<script lang="ts">
    import {Canvas, InteractiveObject, OrbitControls} from '@threlte/core'
    import {spring} from 'svelte/motion'
    import {degToRad} from 'three/src/math/MathUtils'
    import Sidebar from "../components/Sidebar.svelte"
    import {getClient, query, setClient} from 'svelte-apollo'
    import {GET_SHIP} from "./queries";
    // import {client} from "../hooks.client";

    const scale = spring(2);

    const client = getClient()
    const ships = query(GET_SHIP);

/*    function reload() {
        ships.refetch();
    }*/

    $: ships.refetch()
    // console.log($ships.data)
</script>

<div class="flex flex-col h-screen w-screen">
  <div class="text-center w-auto">
    <h1 class="text-3xl font-bold underline ">Welcome to TransVib</h1>
    <ul>
      {#if $ships.loading}
        <li>Loading...</li>
      {:else if $ships.error}
        <li>ERROR: {$ships.error.message}</li>
      {:else}
        Ship: {$ships.data.getShip.title}
      {/if}
    </ul>
  </div>
  <div class="flex flex-row w-full h-full">
    <Sidebar ships={$ships.data.getShip.frames}/>
    <div class="basis-3/4 grow">
      <Canvas>
        <T.PerspectiveCamera makeDefault position={[10, 10, 10]} fov={24}>
          <OrbitControls maxPolarAngle={degToRad(80)} enableZoom={false} target={{ y: 0.5 }}/>
        </T.PerspectiveCamera>

        <T.DirectionalLight castShadow position={[3, 10, 10]}/>
        <T.DirectionalLight position={[-3, 10, -10]} intensity={0.2}/>
        <T.AmbientLight intensity={0.2}/>

        <!-- Cube -->
        <T.Group scale={$scale}>
          <T.Mesh position.y={0.5} castShadow let:ref>
            <!-- Add interaction -->
            <InteractiveObject
                    object={ref}
                    interactive
                    on:pointerenter={() => ($scale = 2)}
                    on:pointerleave={() => ($scale = 1)}
            />

            <T.BoxGeometry/>
            <T.MeshStandardMaterial color="#333333"/>
          </T.Mesh>
        </T.Group>

        <!-- Floor -->
        <T.Mesh receiveShadow rotation.x={degToRad(-90)}>
          <T.CircleGeometry args={[3, 72]}/>
          <T.MeshStandardMaterial color="white"/>
        </T.Mesh>
      </Canvas>
    </div>
  </div>
</div>