from ast import literal_eval
from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
from datetime import datetime
from urllib import parse
from typing import List, Dict, Optional

class SubtaskInput(BaseModel):
    """Input for Subtasks of Main Task"""
    task: str = Field(
        ...,
        description="Task description for this subtask"
    )
    people: str = Field(
        ...,
        description="The number of people to complete this task"
    )
    startTime: str = Field(
        ...,
        description="Start time of this task"
    )
    endTime: str = Field(
        ...,
        description="End time of this task"
    )
    
class ScheduleGenerateInput(BaseModel):
    """Input for Schedule Generate."""
    main_task: str = Field(
        ...,
        description="Main task symbol for Schedule"
    )
    deadline: str = Field(
        ...,
        description="Time limit for complete all Main tasks and Subtasks"
    )
    subtasks: List[SubtaskInput] = Field(
        ...,
        description="Subtasks list for the main task"
    )
    
class ScheduleTool(BaseTool):
    name = "create_task_schedule"
    description =f"""
    Generate Task Schedule from text.
    According time limit and the number of people to schedule and distribute tasks.
    Start time and end time format should be like 'MM-DD'.
    Current time {datetime.now()}.
    """

    def _run(self, main_task: str, deadline: str, subtasks: List[SubtaskInput]):
        print(main_task)
        print(deadline)
        print(subtasks)
        output = {
            "Main_task": main_task,
            "Subtasks": []
        }

        # Ensure subtasks is a list of dictionaries
        if isinstance(subtasks, dict):
            subtasks = [subtasks]

        for subtask in subtasks:
            subtask_info = {
                "Task": subtask['task'],
                "People": subtask['people'],
                "Start_time": subtask['startTime'],
                "End_time": subtask['endTime']
            }
            output["Subtasks"].append(subtask_info)
        
        print("生成行程表")
        print(output)
        return output

    args_schema: Optional[Type[BaseModel]] = ScheduleGenerateInput