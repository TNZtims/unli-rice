default_report = """
Accomplishment Report

Web Scraping Automation:
Successfully developed multiple web scraping scripts using Puppeteer and Cheerio for extracting detailed product information, including specifications, pricing, and images, from e-commerce websites like Sockwell, Footmates, and Old Friend Footwear.

Data Cleanup and Formatting:
Implemented efficient data extraction and cleanup processes, removing unnecessary newline characters and extra spaces, ensuring clean and structured data output.

Transition to Cheerio:
Converted Puppeteer-based scripts to Cheerio for faster scraping, improving performance in scraping product details and subheaders from web pages.

Browser Automation Enhancements:
Integrated the Stealth plugin with Puppeteer to handle automated browser interactions more reliably, including tasks such as logging in to websites and handling hidden elements.

API Integration & Middleware Improvements:
Enhanced the functionality of the makeApiRequest function in React components, improving error handling by adding navigation to the /login route on error conditions.
"""

default_code = """
import React, { useState } from 'react'

const TodoItem = ({ task, index, completeTask, removeTask }) => {
  return (
    <div style={{ textDecoration: task.completed ? 'line-through' : '' }} className='todo-item'>
      {task.text}
      <div>
        <button onClick={() => completeTask(index)}>{task.completed ? 'Undo' : 'Complete'}</button>
        <button onClick={() => removeTask(index)}>Delete</button>
      </div>
    </div>
  )
}

const TodoForm = ({ addTask }) => {
  const [value, setValue] = useState('')

  const handleSubmit = e => {
    e.preventDefault()
    if (!value) return
    addTask(value)
    setValue('')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type='text'
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder='Add a new task'
      />
      <button type='submit'>Add</button>
    </form>
  )
}

const TodoList = () => {
  const [tasks, setTasks] = useState([
    { text: 'Learn React', completed: false },
    { text: 'Build a Todo App', completed: false },
    { text: 'Write clean code', completed: false }
  ])

  const addTask = text => {
    const newTasks = [...tasks, { text, completed: false }]
    setTasks(newTasks)
  }

  const completeTask = index => {
    const newTasks = [...tasks]
    newTasks[index].completed = !newTasks[index].completed
    setTasks(newTasks)
  }

  const removeTask = index => {
    const newTasks = [...tasks]
    newTasks.splice(index, 1)
    setTasks(newTasks)
  }

  return (
    <div className='todo-list'>
      <h1>Todo List</h1>
      {tasks.map((task, index) => (
        <TodoItem
          key={index}
          index={index}
          task={task}
          completeTask={completeTask}
          removeTask={removeTask}
        />
      ))}
      <TodoForm addTask={addTask} />
    </div>
  )
}

export default TodoList
"""