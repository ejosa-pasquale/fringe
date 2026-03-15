from __future__ import annotations

import streamlit as st

from src.ui_car import render_car_page
from src.ui_charging import render_charging_page
from src.ui_home import render_home

st.set_page_config(
    page_title="Fleet & Charging Suite",
    page_icon="🚗",
    layout="wide",
)

home_page = st.Page(render_home, title="Home", icon="🏠", default=True)
car_page = st.Page(render_car_page, title="Fringe benefit auto aziendali", icon="🚗")
charging_page = st.Page(render_charging_page, title="DM 25.10.2025 - Decreto Requisiti Minimi", icon="🔌")

nav = st.navigation([home_page, car_page, charging_page], position="sidebar")

with st.sidebar:
    st.markdown("## Fleet & Charging Suite")
    st.caption("Base pronta per GitHub")

nav.run()
