<script>
    import "../app.css";
    import {ApolloClient, InMemoryCache} from "@apollo/client";
    import {setClient} from "svelte-apollo";

    const client = new ApolloClient({
        uri: 'http://0.0.0.0:5000/graphql',
        cache: new InMemoryCache()
    });

    setClient(client);
</script>

<slot/>