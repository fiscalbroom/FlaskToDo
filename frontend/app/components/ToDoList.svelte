<script>
    import { onMount } from 'svelte';
    import { ToDoService } from '../services/todo.service';
    import ToDoItem from './ToDoItem.svelte';

    let isReady = false,
        isLoading = false,
        todos = [],
        newText = '',
        inputE1;

    onMount(async () => {
        try {
            todos = await ToDoService.getAll();
        }catch (error){
            console.error(error);
        }finally{
            isReady = true;
        }
    });

    async function handleSubmit(event){
        if (newText.length === 0) return;

        isLoading = true;
        try{
            const newToDo = await ToDoService.add(newText);
            todos = [newToDo, ...todos];
            newText = '';
            setTimeout(function() {
                inputE1.focus();
            }, 1);
            }catch (error){
                console.error(error);
        }finally{
            isLoading = false;
        }
    }

    async function handleDelete(event){
        try {
            const {detail: todoId} = event;

            await ToDoService.delete(todoId);
            todos = todos.filter(todo => todo.id !== todoId);
        }catch (error){
            console.error(error);
        }
    }

    async function handleEdit(event){
        try {
            const {detail: todo} = event;

            await ToDoService.update(todo);
            todos = todos.map(td => {
                if (td.id !== todo.id) {
                    return td;
                }
                return {...td, ...todo};
            })
        }catch (error){
            console.error(error);
        }
    }
</script>


<section class="todo-list-container">
    <h1 class="todo-list-header">ToDo List</h1>

    {#if !isReady}
        <h2 class="todo-list-header">Caricamento...</h2>
        {/if}

    {#if isReady}
        <form class="todo-list-form" on:submit|preventDefault={handleSubmit}>
            <input
                class="todo-list-input"
                type="text"
                bind:value={newText}
                placeholder="Inserisci un nuovo ToDo"
                ref={inputE1}
            />
            <button class="todo-list-button" type="submit" disabled={isLoading}>
                {#if isLoading}
                    Caricamento...
                    {:else}
                    Aggiungi
                {/if}
            </button>
        </form>

        <ul class="todo-list">
            {#each todos as todo}
                <ToDoItem
                    todo={todo}
                    on:delete={handleDelete}
                    on:edit={handleEdit}
                />
            {/each}
        </ul>
    {/if}
</section>