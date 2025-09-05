import streamlit as st
from langchain_ollama import OllamaLLM
import datetime

@st.cache_resource
def load_model():
    return OllamaLLM(model='llama3', temperature=1.5)

llm = load_model()
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []
if 'ai_suggestion' not in st.session_state:
    st.session_state.ai_suggestion = ''

st.title('AI-Powered To-Do Manager')
st.subheader('Your Tasks')
if not st.session_state.tasks:
    st.info('No tasks added yet. Start by adding a new task below!')
else:
    # Create a list to track which tasks to complete/delete
    tasks_to_complete = []
    tasks_to_delete = []
    
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        
        with col1:
            # Use task content as part of key to make it unique
            if st.checkbox('', key=f'complete_{i}_{hash(task)}', help='Mark as complete'):
                tasks_to_complete.append(i)
        
        with col2:
            st.write(f'{i + 1}. {task}')
        
        with col3:
            if st.button('Delete', key=f'delete_{i}_{hash(task)}', help='Delete task'):
                tasks_to_delete.append(i)
    
    # Process completions (in reverse order to maintain indices)
    for i in sorted(tasks_to_complete, reverse=True):
        completed_task = st.session_state.tasks.pop(i)
        st.session_state.completed_tasks.append({
            'task': completed_task,
            'completed_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        st.success(f'ompleted: {completed_task}')
        st.rerun()
    
    # Process deletions (in reverse order to maintain indices)  
    for i in sorted(tasks_to_delete, reverse=True):
        removed = st.session_state.tasks.pop(i)
        st.success(f'Deleted: {removed}')
        st.rerun()


st.subheader('Add New Task')
col1, col2 = st.columns([0.8, 0.2])

with col1:
    task_input = st.text_input('Enter a new task:', placeholder='e.g., Buy groceries')

with col2:
    add_button = st.button('Add Task', type='primary')

if add_button and task_input.strip():
    if task_input.strip() not in st.session_state.tasks:
        st.session_state.tasks.append(task_input.strip())
        st.success('Task added successfully!')
        st.rerun()
    else:
        st.warning('Task already exists!')
elif add_button:
    st.warning('Please enter a task!')
if st.session_state.tasks:
    st.subheader('Quick Actions')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('Clear All Tasks', type='secondary'):
            if st.session_state.tasks:
                st.session_state.completed_tasks.extend([
                    {'task': task, 'completed_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
                    for task in st.session_state.tasks
                ])
                st.session_state.tasks.clear()
                st.success('All tasks marked as completed!')
                st.rerun()
    
    with col2:
        task_to_update = st.selectbox('Select task to update:', 
                                    options=range(len(st.session_state.tasks)),
                                    format_func=lambda x: f'{x+1}. {st.session_state.tasks[x]}')
        
    with col3:
        new_task_value = st.text_input('New task value:', key='update_input')
        if st.button('Update Selected') and new_task_value.strip():
            st.session_state.tasks[task_to_update] = new_task_value.strip()
            st.success('Task updated!')
            st.rerun()

st.subheader('AI Task Suggestions')

col1, col2 = st.columns([0.5, 0.5])

with col1:
    if st.button('Get AI Suggestion', type='secondary'):
        with st.spinner('AI is thinking...'):
            try:
                current_tasks_context = ''
                if st.session_state.tasks:
                    current_tasks_context = f'\nCurrent tasks: {', '.join(st.session_state.tasks[:3])}'
                
                suggestion = llm.invoke(f'''
                Suggest one practical, actionable to-do list item for daily productivity.
                Keep it concise (2-5 words).
                Make it different from common tasks like 'check email' or 'make calls'.
                Focus on health, productivity, or personal growth.
                {current_tasks_context}
                
                Reply with only the task text, no explanation.
                ''')
                
                st.session_state.ai_suggestion = suggestion.strip()
                
            except Exception as e:
                st.error(f'AI suggestion failed: {str(e)}')
                st.session_state.ai_suggestion = 'Review daily goals'

with col2:
    if st.session_state.ai_suggestion:
        st.info(f'Suggestion: {st.session_state.ai_suggestion}')
        if st.button('Add AI Suggestion', type='primary'):
            if st.session_state.ai_suggestion not in st.session_state.tasks:
                st.session_state.tasks.append(st.session_state.ai_suggestion)
                st.success('AI task added!')
                st.session_state.ai_suggestion = ''  # Clear suggestion
                st.rerun()
            else:
                st.warning('Task already exists!')

# --- Completed Tasks ---
if st.session_state.completed_tasks:
    with st.expander('Completed Tasks'):
        for completed in reversed(st.session_state.completed_tasks[-10:]):
            st.text(f'✓ {completed['task']} (completed: {completed['completed_at']})')
        
        if st.button('Clear Completed History'):
            st.session_state.completed_tasks.clear()
            st.success('Completed tasks history cleared!')
            st.rerun()

