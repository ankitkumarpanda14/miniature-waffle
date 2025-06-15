from ollama import chat
from pydantic import BaseModel
from typing import List, Dict
from enum import Enum
import streamlit as st
import uuid

MODEL = "llama3.2:3b"

class TimeSlot(str, Enum):
    morning = "morning"
    afternoon = "afternoon"
    evening = "evening"

class budgetMinMax(str, Enum):
    min = "min"
    max = "max"

class Destination(BaseModel):
    city_name: str
    reason: str
    nearest_airport: str

class Destinations(BaseModel):
    destinations: List[Destination]

class DayPlan(BaseModel):
    activity: str
    details: str

class Day(BaseModel):
    day: int
    date: str
    dayplan: Dict[TimeSlot, DayPlan]

class Itinerary(BaseModel):
    days: List[Day]

class BudgetBreakdown(BaseModel):
    tripDetails: Dict
    costBreakdown: Dict
    totalEstimatedCost: Dict[budgetMinMax, float]
    notes: List[str]

class SafetyInfo(BaseModel):
    safety_tips: Dict[str, List[str]]
    emergency_info: Dict[str, Dict[str, str]]
    apps: List[Dict[str, str]]
    disclaimer: str

class FullTrip(BaseModel):
    destination: str
    itinerary: Itinerary
    budget: BudgetBreakdown
    safety: SafetyInfo

def generate_structred_output(prompt, schema):
    response = chat(
        messages= [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        model=MODEL,
        format=schema,
    )
    return response

def get_destinations(user_input: str) -> Destinations:
    prompt = f"""Suggest 3 compelling travel destinations based on this user request: \
                {user_input}"""
    response = generate_structred_output(prompt, Destinations.model_json_schema())
    possible_destinations = Destinations.model_validate_json(response.message.content)
    return possible_destinations

def generate_itinerary(destination: str) -> Itinerary:
    prompt = f"""
        Generate a highly detailed 3-day itinerary for a trip to {destination}.
        For each day, provide a specific date and include three parts: \
            morning, afternoon, and evening. Provide links for activities and \
                hotel bookings from reputed known websites like makemytrip, thrillopia, easemytrip, government websites etc"""
    response = generate_structred_output(prompt, Itinerary.model_json_schema())
    itinerary = Itinerary.model_validate_json(response.message.content)
    return itinerary

def estimate_budget(destination: str) -> BudgetBreakdown:
    prompt = f"""
                Estimate a comprehensive travel budget for a 3-day trip to {destination}. \
                Provide a detailed breakdown of costs (e.g., flights, accommodation, food,\
                      activities) and a total estimated cost range (min and max). \
                        Please provide all numbers in INR. Consider the origin destination to be bangalore always.
            """
    response = generate_structred_output(prompt, BudgetBreakdown.model_json_schema())
    budget = BudgetBreakdown.model_validate_json(response.message.content)
    return budget

def get_safety_info(destination: str) -> SafetyInfo:
    prompt = f"Provide essential safety information for a trip to {destination}. Include \
        general safety tips, local emergency numbers, recommendations for useful apps, \
            and a standard disclaimer."
    response = generate_structred_output(prompt, SafetyInfo.model_json_schema())
    safety_info = SafetyInfo.model_validate_json(response.message.content)
    return safety_info

st.set_page_config(page_title="Agentic Travel Planner", layout="wide")
st.title("🌍 Personal Travel Planner")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

user_input = st.text_area("Tell me about your dream trip:", placeholder="e.g., 'A relaxing 3-day beach getaway in Southeast Asia with great food' or 'An adventurous mountain hiking trip in Europe'")

if st.button("Plan My Trip"):
    if not user_input:
        st.warning("Please tell me about your dream trip first")
    else:
        with st.spinner("Generating your perfect trip..."):
            dests = get_destinations(user_input)
            if not dests:
                st.error("Could not generate destinations. Please try again.")
                st.stop()
            
            best_dest = dests.destinations[0].city_name
            itinerary = generate_itinerary(best_dest)
            budget = estimate_budget(best_dest)
            safety = get_safety_info(best_dest)
            trip = FullTrip(destination=best_dest, itinerary=itinerary, budget=budget, safety=safety)

            st.subheader(f"📍 Destination: {trip.destination}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🗓️ Itinerary")

                for day in trip.itinerary.days:
                    # st.markdown(f"**Day {day.day}:** {day.date}")
                    with st.expander(f"**Day {day.day}:** {day.date}"):
                        st.markdown(f"**Morning** {day.dayplan.get(TimeSlot.morning).activity}")
                        st.markdown(f"**Details** {day.dayplan.get(TimeSlot.morning).details}")
                        st.markdown(f"**Afternoon** {day.dayplan.get(TimeSlot.afternoon).activity}")
                        st.markdown(f"**Details** {day.dayplan.get(TimeSlot.afternoon).details}")
                        st.markdown(f"**Evening** {day.dayplan.get(TimeSlot.evening).activity}")
                        st.markdown(f"**Details** {day.dayplan.get(TimeSlot.evening).details}")

            with col2:
                st.markdown("### 💰 Budget")
                b = trip.budget
                st.markdown(f"**Travel Styles:** {b.tripDetails.get('travelStyle', 'N/A')}")
                st.metric("Estimated Cost", f"₹{b.totalEstimatedCost.get('min', 0)} - ₹{b.totalEstimatedCost.get('max', 0)}")
                with st.expander("Cost Breakdown and Notes"):
                    st.json(b.costBreakdown)
                    for note in b.notes:
                        st.markdown(f"- {note}")

            st.markdown("### 🛡️ Safety Information")
            for sec, tips in trip.safety.safety_tips.items():
                with st.expander(sec.replace("_", " ").title()):
                    for tip in tips:
                        st.markdown(f"- {tip}")

            with st.expander("🚨 Emergency Info"):
                for k, v in trip.safety.emergency_info.items():
                    st.markdown(f"**{k.title()}**: {v}")

            with st.expander("📱 Useful Apps"):
                for app in trip.safety.apps:
                    try:
                        st.markdown(f"- {app}")
                    except:
                        st.markdown("Could not get safety recommended apps")
            st.caption(trip.safety.disclaimer)
# destinations = get_destinations("3-day Hiking Trip in North India")
# print(destinations.destinations[0].city_name)
# itinerary = generate_itinerary(destinations.destinations[0].city_name)
# print(itinerary.days[0].day)
# print(itinerary.days[0].date)
# print(itinerary.days[0].dayplan)
# estimated_budget = estimate_budget(destinations.destinations[0].city_name)
# print(estimated_budget.totalEstimatedCost)
# safety = get_safety_info(destinations.destinations[0].city_name)
# print(safety.safety_tips)

