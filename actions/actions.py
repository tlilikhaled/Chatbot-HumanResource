
from typing import Any, Text, Dict, List
from rasa_sdk.types import DomainDict
from rasa_sdk import Action, Tracker, FormValidationAction
from dateutil import parser
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)


from actions.custom_forms import CustomFormValidationAction
from database.connection_db import (
    active_dev, 
    active_qa,
    active_devops,
    active_support,
    List_resources_project,
    list_known_projects_Id, 
    List_employees_project
)

class ActionListResource(Action):
    """ Know list resources with projectId"."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_List_resources"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        """Executes the action"""
        slots = {
            "id": None,
        }
        
        Id = tracker.get_slot("id")
         
        Id1 = str(Id)   
        known_Id = list_known_projects_Id()
        if Id is not None and Id1  in known_Id:
            res = List_resources_project(Id)
            dispatcher.utter_message(text=f" List resources in your project : {res} ") 
            dispatcher.utter_message(response="utter_ask_whatelse") 
        else:
            dispatcher.utter_message(response="utter_unknown_project_id")

        return [SlotSet(slot, value) for slot, value in slots.items()]
   
class ActionListEmpWithProjectId(Action):
    """ Know list employees with projectId"."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_List_activeId"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        """Executes the action"""
        slots = {
            "project_id": None,
        }
       
        Id = tracker.get_slot("project_id")
        
        Id1 = str(Id)   
        known_Id = list_known_projects_Id()
        if Id is not None and Id1  in known_Id:
            res = List_employees_project(Id)
            dispatcher.utter_message(text=f" The active employee are : {res} ") 
            dispatcher.utter_message(response="utter_ask_whatelse") 
        else:
            dispatcher.utter_message(response="utter_unknown_project_id")

        return [SlotSet(slot, value) for slot, value in slots.items()]



class ActionKnowActiveEmployeeWithGrade(Action):
    """Know active employee with grade"."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_grade_employee"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        """Executes the action"""
        slots = {
            "grade": None,
        }

              
        
        if tracker.get_slot("grade") == "Developer":
            List_dev = active_dev()
            dispatcher.utter_message(text=f" The List active employees with grade Developer is {List_dev} ")
            dispatcher.utter_message(response="utter_ask_whatelse") 
        if tracker.get_slot("grade") == "Quality":
            List_qa = active_qa()
            dispatcher.utter_message(text=f" The List active employees with grade Quality is  {List_qa} ")
            dispatcher.utter_message(response="utter_ask_whatelse") 
        if tracker.get_slot("grade") == "DevOps":
            List_devops = active_devops()
            dispatcher.utter_message(text=f" The List active employees with grade Devops is  {List_devops} ")
            dispatcher.utter_message(response="utter_ask_whatelse") 
        if tracker.get_slot("grade") == "IT Support":
            List_support = active_support()
            dispatcher.utter_message(text=f" The List active employees with grade Support is  {List_support} ")
            dispatcher.utter_message(response="utter_ask_whatelse") 
      


        return [SlotSet(slot, value) for slot, value in slots.items()]

    
class ValidateKnowGradeForm(CustomFormValidationAction):
    """Validates Slots of the know_grade_form"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "validate_know_grade_form"
    
    async def validate_grade(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validates value of 'grade' slot"""

        List = ["Developer", "Quality","DevOps","IT Support"]
      
        if value in List:
            return {"grade": value}
        
        dispatcher.utter_message(response="utter_unknown_grade")
        return {"grade": None}


    

class ActionSessionStart(Action):
    """Executes at start of session"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_session_start"

    @staticmethod
    def _slot_set_events_from_tracker(
        tracker: "Tracker",
    ) -> List["SlotSet"]:
        """Fetches SlotSet events from tracker and carries over keys and values"""

        # when restarting most slots should be reset
        relevant_slots = ["grade"]

        return [
            SlotSet(
                key=event.get("name"),
                value=event.get("value"),
            )
            for event in tracker.events
            if event.get("event") == "slot" and event.get("name") in relevant_slots
        ]
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Executes the custom action"""
        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        events.extend(self._slot_set_events_from_tracker(tracker))


        # add `action_listen` at the end
        events.append(ActionExecuted("action_listen"))

        return events
class ActionRestart(Action):
    """Executes after restart of a session"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_restart"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """Executes the custom action"""
        return [Restarted(), FollowupAction("action_session_start")]
