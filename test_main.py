import pytest
from main import TaskManager

@pytest.fixture
def task_manager():
    """Create a temporary in-memory TaskManager for testing."""
    return TaskManager(":memory:")

def test_add_task(task_manager):
    """Test adding a task."""
    task_manager.add_task("Test task", "2025-04-01")
    tasks = task_manager.get_tasks()
    assert len(tasks) == 1
    assert tasks[0][1] == "Test task"
    assert tasks[0][2] == "2025-04-01"
    assert tasks[0][3] == "À faire"

def test_add_valid_task(task_manager):
    """Test adding a valid task."""
    task_manager.add_task("Acheter du lait", "2025-05-01")
    tasks = task_manager.get_tasks()
    assert len(tasks) == 1
    assert tasks[0][1] == "Acheter du lait"
    assert tasks[0][2] == "2025-05-01"
    assert tasks[0][3] == "À faire"

def test_add_task_invalid_date(task_manager):
    """Test adding a task with an invalid date."""
    with pytest.raises(ValueError):
        task_manager.add_task("Faire le ménage", "01-05-2025")  # Invalid date format

def test_update_task_status(task_manager):
    """Test updating the status of a task."""
    task_manager.add_task("Apprendre Python", "2025-06-10")
    task_id = task_manager.get_tasks()[0][0]
    task_manager.update_task_status(task_id, "Terminé")
    updated_task = task_manager.get_tasks()[0]
    assert updated_task[3] == "Terminé"

def test_delete_task(task_manager):
    """Test deleting a task."""
    task_manager.add_task("Jouer au foot", "2025-07-01")
    task_id = task_manager.get_tasks()[0][0]
    task_manager.delete_task(task_id)
    assert len(task_manager.get_tasks()) == 0

def test_empty_description(task_manager):
    """Test that a task cannot be added without a description."""
    with pytest.raises(ValueError):
        task_manager.add_task("", "2025-08-01")

def test_list_tasks_sorted(task_manager):
    """Test that tasks are sorted by due date."""
    task_manager.add_task("Tâche 1", "2025-09-01")
    task_manager.add_task("Tâche 2", "2025-08-01")
    tasks = task_manager.get_tasks()
    assert tasks[0][1] == "Tâche 2"
    assert tasks[1][1] == "Tâche 1"

