import unittest
from app.tasks.scheduler import create_task


def test_task():
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)


if __name__ == "__main__":
    unittest.main()
