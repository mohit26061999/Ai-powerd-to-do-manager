from langchain_ollama import OllamaLLM
llm = OllamaLLM(model='llama3',temperature=0.5)
tasks = []
def show_task():
    if not tasks:
        print('No task added yet')
    else:
        for i, task in enumerate(tasks,1):
            print(f'{i}. {task}')

            
def add_task():
    task = input('enter your task: ')
    if task not in tasks:
        tasks.append(task)
        print('Task added sucessfully')
    else:
        print('task already exist')

def update_task():
    show_task()
    num = int(input('Enter task number to update: ')) - 1
    if 0 <= num < len(tasks):
        new_task = input('Enter new task: ')
        tasks[num] = new_task
        print('Task updated!')
    else:
        print('Invalid task number')
def delete_task():
    show_task()
    num = int(input('Enter task number to delete: '))-1
    if 0 <= num < len(tasks):
        tasks.pop(num)
        print('Task deleted')
    else:
        print('Invalid task number')

def ai_generated_task():
    suggestion = llm.invoke("""Suggest one short, ready-to-add to-do list item. 
Keep it very concise (2–4 words). 
Do not explain, do not use "write", "do", or "make". 
Reply with only the task text.""")
    task_line = suggestion.strip()
    print('\n Ai Suggest', suggestion)
    choice = input('Do you want to add this task (y/n)')
    if choice.lower() == 'y':
        if task_line not in tasks:
            tasks.append(task_line)
            print('Task Added Sucessfully')
        else:
            print('Task already added')

def main():
    while True:
        print("\n--- To-Do Manager ---")
        print("1. View tasks")
        print("2. Add task")
        print("3. Update task")
        print("4. Ai Suggestion")
        print("5. Delete task")
        print("6. Exit")

        choice = input('choose an option: ')

        if choice =='1':
            show_task()

        elif choice == '2':
            add_task()
        elif choice =='3':
            update_task()
        elif choice == '4':
            ai_generated_task()
        elif choice == '5':
            delete_task()
        elif choice=='6':
            break
        else:
            print('Invalid Option')
main()

