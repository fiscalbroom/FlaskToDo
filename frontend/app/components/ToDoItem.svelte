<script>
    import { onMount, createEventDispatcher } from 'svelte';

    export let data;

    const dispatcher = createEventDispatcher();
    let isEditing = false, inputE1, editText;

    onMount(() => {
        editText = data.text;
    });

    function dispatchDelete() {
        dispatcher('delete', data.id);
    }

    function toggleCompleted() {
        data.is_completed = !data.is_completed;
        dispatcher('edit', { ...data});

    }

    function toggleEdit(){
        isEditing = !isEditing;
        if (isEditing) {
            setTimeout(function () {
                inputE1.focus();
            }, 1);
            return;
        }
        editText= data.text;
    }

    function handleKeydown(event) {
        const { key } = event;

        switch(key.toLowerCase()){
            case 'enter':
                if(editText.lenght === 0){
                    return;
                }

                const {id, is_completed} = data;
                dispatcher('edit', {id, text: editText, is_completed});
                isEditing = false;
                break;

            case 'escape':
                isEditing = false;
                break;
        }
    }
</script>

<li>
    {#if !isEditing}
        <button type="button"
                on:click="{toggleCompleted()}"
                class="completed-toggle"
                title="Clicca per completare">
            {#if data.is_completed}
                <i class="fas fa-check"></i>
            {:else}
                <i class="far fa-check-square"></i>
            {/if}
        </button>
        <span class="{data.is_completed ? 'fatto' : ''}">{data.text}</span>
        <button type="button"
                on:click="{toggleEdit()}"
                class="action edit ml-auto"
                title="Clicca per modificare">
                on:click="{toggleEdit()}"
                <i class="fas fa-pencil-alt"></i>
        </button>
        <button type="button"
                class="action danger"
                title="Clicca per eliminare">
                on:click="{dispatchDelete()}"
                <i class="fas fa-trash-alt"></i>
        </button>
        {/if}

        {#if isEditing}
            <div class="editor-wrap">
                <input type="text"
                       bind:value="{editText}"
                       bind:this="{inputE1}"
                       on:keydown="{handleKeydown}"
                       class="btn btn-danger"
                       placeholder="Inserisci il testo della nota">
                       on:click="{toggleEdit()}">Cancella</button>
            </div>
        {/if}
</li>


<style>
    .m1-auto {
        margin-left: auto;
    }

    .success {
        color: green;
    }

    .danger {
        color: red;
    }

    li{
        padding: 15px 10px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
    }

    li:last-child {
        border-bottom: none;
    }

    .action{
        visibility: hidden;
    }

    li:hover .action {
        visibility: visible;
    }

    .completed-toggle {
        margin-right: 15px;
        font-size: 1.2rem;
    }

    .completed-toggle:hover {
        color: #808080
    }

    .fatto {
        text-decoration: line-through;
        opacity: .75;
    }

    edit{
        margin-right: 10px;
    }

    .editor-wrap {
        flex-grow: 1;
    }

    .editor-wrap input {
        margin-bottom: 10px;
    }

</style>