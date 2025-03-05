import streamlit as st
from pint import UnitRegistry

# Initialize Unit Registry
ureg = UnitRegistry()

# Define available unit categories
unit_categories = {
    "Length": ["meters", "kilometers", "miles", "feet", "inches", "centimeters"],
    "Weight": ["grams", "kilograms", "pounds", "ounces"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
}

def convert_units(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value, "Same unit, no conversion needed"
    
    if from_unit in ["celsius", "fahrenheit", "kelvin"]:
        # Special handling for temperature conversions
        if from_unit == "celsius":
            if to_unit == "fahrenheit":
                return (value * 9/5) + 32, "(value × 9/5) + 32"
            elif to_unit == "kelvin":
                return value + 273.15, "value + 273.15"
        elif from_unit == "fahrenheit":
            if to_unit == "celsius":
                return (value - 32) * 5/9, "(value - 32) × 5/9"
            elif to_unit == "kelvin":
                return (value - 32) * 5/9 + 273.15, "((value - 32) × 5/9) + 273.15"
        elif from_unit == "kelvin":
            if to_unit == "celsius":
                return value - 273.15, "value - 273.15"
            elif to_unit == "fahrenheit":
                return (value - 273.15) * 9/5 + 32, "((value - 273.15) × 9/5) + 32"
    else:
        # General conversion using pint
        converted_value = (value * ureg(from_unit)).to(to_unit).magnitude
        formula = f"Multiply by {(ureg(to_unit) / ureg(from_unit)).magnitude:.6g}"
        return converted_value, formula

# Streamlit UI
st.title("🌍 Google Unit Converter")
st.write("Convert between different units easily!")

# Select category
category = st.selectbox("Select Unit Category", list(unit_categories.keys()))

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    value = st.number_input("Enter value", value=1.0, step=0.1, key="input_value")
    from_unit = st.selectbox("From Unit", unit_categories[category], key="from_unit")

with col2:
    st.markdown("<h2 style='text-align: center;'>=</h2>", unsafe_allow_html=True)

with col3:
    to_unit = st.selectbox("To Unit", unit_categories[category], key="to_unit")
    converted_value, formula = convert_units(value, from_unit, to_unit)
    st.number_input("Converted value", value=converted_value, step=0.1, key="output_value", disabled=True)

# Display formula
st.markdown(f"<p style='background-color:#FF5733; padding:5px; display:inline-block; border-radius:5px;'>Formula</p> {formula}", unsafe_allow_html=True)