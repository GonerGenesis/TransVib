<script lang="ts">
	import { T, Canvas, InteractiveObject, OrbitControls} from '@threlte/core'
	import { spring } from 'svelte/motion'
	import { degToRad } from 'three/src/math/MathUtils'
	import Sidebar from "../components/Sidebar.svelte";
	import {ApolloClient, gql} from '@apollo/client';
	import {setClient, getClient, query} from 'svelte-apollo';

	const scale = spring(2)
	const client = new ApolloClient({uri: 'https://geodb-cities-graphql.p.rapidapi.com/'});
setClient(client);
</script>

<div class="h-screen">
	<div class="text-center w-auto">
		<h1 class="text-3xl font-bold underline ">Welcome to SvelteKit</h1>
		<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
	</div>
	<div class="flex flex-row h-full w-full">
		<Sidebar />
		<Canvas class="h-full basis-3/4">
			<T.PerspectiveCamera makeDefault position={[10, 10, 10]} fov={24}>
				<OrbitControls maxPolarAngle={degToRad(80)} enableZoom={false} target={{ y: 0.5 }} />
			</T.PerspectiveCamera>

			<T.DirectionalLight castShadow position={[3, 10, 10]} />
			<T.DirectionalLight position={[-3, 10, -10]} intensity={0.2} />
			<T.AmbientLight intensity={0.2} />

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

					<T.BoxGeometry />
					<T.MeshStandardMaterial color="#333333" />
				</T.Mesh>
			</T.Group>

			<!-- Floor -->
			<T.Mesh receiveShadow rotation.x={degToRad(-90)}>
				<T.CircleGeometry args={[3, 72]} />
				<T.MeshStandardMaterial color="white" />
			</T.Mesh>
		</Canvas>
	</div>
</div>