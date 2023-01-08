<script>
    import "../app.css";
    import {createClient, setContextClient} from '@urql/svelte'

    const client = createClient({
        url: `http://0.0.0.0:5000/graphql`,
    })
    setContextClient(client)
</script>

<slot/>