// Task Tracker Frontend - Handles all interactions with the REST API

const API_BASE = 'http://localhost:8000/api/v1';
const apiStatusEl = document.getElementById('api-status');
const createForm = document.getElementById('create-form');
const createMessageEl = document.getElementById('create-message');
const tasksContainer = document.getElementById('tasks-container');

// Check API health on page load
window.addEventListener('load', () => {
    checkApiHealth();
    loadTasks();
});

// Handle task creation form submission
createForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('title-input').value.trim();
    const description = document.getElementById('description-input').value.trim();
    
    if (!title) {
        showMessage('Please enter a task title', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/tasks/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        showMessage('Task created successfully!', 'success');
        createForm.reset();
        loadTasks();
    } catch (error) {
        showMessage(`Failed to create task: ${error.message}`, 'error');
    }
});

// Check API health status
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            setApiStatus('healthy');
        } else {
            setApiStatus('error');
        }
    } catch (error) {
        setApiStatus('error');
    }
}

// Update API status indicator
function setApiStatus(status) {
    apiStatusEl.textContent = status === 'healthy' ? '✓ API Connected' : '✗ API Offline';
    apiStatusEl.className = `status-badge ${status}`;
}

// Load all tasks from API
async function loadTasks() {
    try {
        const response = await fetch(`${API_BASE}/tasks/`);
        if (!response.ok) throw new Error(`Failed to load tasks: ${response.status}`);
        
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        tasksContainer.innerHTML = `<p class="loading">Error loading tasks: ${error.message}</p>`;
    }
}

// Render tasks to the DOM
function renderTasks(tasks) {
    if (tasks.length === 0) {
        tasksContainer.innerHTML = '<p class="loading">No tasks yet. Create one above!</p>';
        return;
    }
    
    tasksContainer.innerHTML = tasks.map(task => `
        <div class="task-item">
            <div class="task-header">
                <div class="task-title">${escapeHtml(task.title)}</div>
                <span class="task-status ${task.status}">${formatStatus(task.status)}</span>
            </div>
            
            ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : '<div class="task-description empty">No description</div>'}
            
            <div class="task-meta">
                <span>Created: ${formatDate(task.created_at)}</span>
                <span>Updated: ${formatDate(task.updated_at)}</span>
            </div>
            
            <div class="task-actions">
                <select onchange="updateTaskStatus(${task.id}, this.value)" ${isStatusDone(task.status) ? 'disabled' : ''}>
                    <option value="">Change status...</option>
                    ${getAvailableTransitions(task.status).map(status => 
                        `<option value="${status}" ${status === task.status ? 'selected' : ''}>${formatStatus(status)}</option>`
                    ).join('')}
                </select>
                <button onclick="deleteTask(${task.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Update task status with validation
async function updateTaskStatus(taskId, newStatus) {
    if (!newStatus) return;
    
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (!response.ok) {
            const error = await response.json();
            showMessage(`Cannot update status: ${error.detail}`, 'error');
            loadTasks(); // Reload to reset select
            return;
        }
        
        showMessage('Task updated successfully!', 'success');
        loadTasks();
    } catch (error) {
        showMessage(`Failed to update task: ${error.message}`, 'error');
    }
}

// Delete a task
async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`Failed to delete task: ${response.status}`);
        }
        
        showMessage('Task deleted successfully!', 'success');
        loadTasks();
    } catch (error) {
        showMessage(`Failed to delete task: ${error.message}`, 'error');
    }
}

// Get available status transitions (per ADR-0001)
function getAvailableTransitions(currentStatus) {
    const transitions = {
        'todo': ['todo', 'in_progress'],
        'in_progress': ['in_progress', 'done'],
        'done': ['done']
    };
    return transitions[currentStatus] || [];
}

// Check if task is in done status (cannot transition forward)
function isStatusDone(status) {
    return status === 'done';
}

// Format status for display
function formatStatus(status) {
    const statusMap = {
        'todo': 'To Do',
        'in_progress': 'In Progress',
        'done': 'Done'
    };
    return statusMap[status] || status;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show message to user
function showMessage(message, type) {
    createMessageEl.textContent = message;
    createMessageEl.className = type;
    setTimeout(() => {
        createMessageEl.className = '';
    }, 5000);
}