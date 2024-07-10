<script>
    import { push } from 'svelte-spa-router'
    import fastapi from "../lib/api"
    import Error from "../components/Error.svelte"

    let error = {detail:[]}
    let system_prompt = ''
    let temperature = 1
    let all_token = true
    let top_p = 1
    let top_k = -1


    function post_question(event) {
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            system_prompt,
            temperature,
            top_p,
            top_k: all_token ? -1 : top_k
        }
        console.info("here is post_question")
        fastapi('post', url, params, 
            (json) => {
                const questionId = json.id; 
                push(`/detail/${questionId}`);
            },
            (json_error) => {
                error = json_error
            }
        )
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">New AI Assistant</h5>
    <Error error={error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">System Prompt</label>
            <textarea type="text" class="form-control" rows="5" bind:value="{system_prompt}"></textarea>
        </div>
        <div class="mb-3">
              <label for="temperature">Temperature<strong id="value1">&nbsp;{temperature}</strong></label> 
              <input type="range" class="form-range" min="0" max="1" step="0.1" bind:value={temperature} oninput="{e => document.getElementById('value1').innerHTML = e.target.value}">
        </div>
        <div class="mb-3">
            <label for="temperature">Top-P<strong id="value2">&nbsp;{top_p}</strong></label>
            <input type="range" class="form-range" min="0" max="1" step="0.05" bind:value={top_p} oninput="{e => document.getElementById('value2').innerHTML = e.target.value}">

        </div>
        <div class="mb-3">
            <label for="temperature">Top-K<strong id="value3">&nbsp;{top_k}</strong></label> 
            <label for="all_token">Consider all tokens</label>
            <input type="checkbox" id="all_token" bind:checked={all_token}>
            <div style="display: {all_token ? 'none': 'block'};">
            <input type="range" class="form-range" min="0" max="50" step="5" bind:value={top_k} oninput={e => document.getElementById('value3').innerHTML = e.target.value}>
        </div>
        <br>
        <br>
        <button class="btn btn-primary" on:click="{post_question}">저장하기</button>
    </form>
</div>
