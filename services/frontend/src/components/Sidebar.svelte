<script lang="ts">
    import {getClient} from "svelte-apollo";

    const client = getClient()



</script>

<div class="h-full text-center min-w-fit w-1/7 shadow-md bg-white inset-y-0 left-0" id="sidenav">
    <p >Frames</p>
    <ul class="relative px-1">
        <li class="relative">
            <span> 1st item </span>
        </li>
        <li class="relative">
            <span> 2nd item </span>
        </li>
    </ul>

</div>