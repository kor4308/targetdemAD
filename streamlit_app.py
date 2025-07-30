with col3.expander("Estimated Quantity Needed to Screen"):
    st.markdown("**Estimated Quantity Needed to Screen - Gender**")
    st.caption("⬇️ List is in order from greatest % population needed to screen")
    total_enroll = st.session_state.get("total_enroll", 1000)

    gender_data = []
    for key in target["Gender"]:
        pct = st.session_state.get(f"gender_{key}", target["Gender"][key])
        target_n = total_enroll * (pct / 100)
        screen_success_rate = st.session_state.get(f"sf_gender_{key}", 100) / 100
        screened_needed = math.ceil(target_n / screen_success_rate) if screen_success_rate > 0 else 0
        eligible_pop = int((target["Gender"].get(key, 100) / 100) * total_disease_pop)
        screen_percent = (screened_needed / eligible_pop) * 100 if eligible_pop > 0 else 0
        gender_data.append((key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop))

    gender_data.sort(key=lambda x: -x[2])
    for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in gender_data:
        st.markdown(f"{key}: {screened_needed:,} ({screen_percent:.3f}%)")
        st.caption(f"Approximately {screen_percent:.3f}% of {key} {disease} population must be screened to enroll target")

    st.markdown("**Estimated Quantity Needed to Screen - Race**")
    st.caption("⬇️ List is in order from greatest % population needed to screen")
    race_data = []
    for key in target["Race"]:
        pct = st.session_state.get(f"race_{key}", target["Race"][key])
        target_n = total_enroll * (pct / 100)
        screen_success_rate = st.session_state.get(f"sf_race_{key}", 100) / 100
        screened_needed = math.ceil(target_n / screen_success_rate) if screen_success_rate > 0 else 0
        eligible_pop = int((target["Race"].get(key, 0) / 100) * total_disease_pop)
        screen_percent = (screened_needed / eligible_pop) * 100 if eligible_pop > 0 else 0
        race_data.append((key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop))

    race_data.sort(key=lambda x: -x[2])
    for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in race_data:
        st.markdown(f"{key}: {screened_needed:,} ({screen_percent:.3f}%)")
        st.caption(f"Approximately {screen_percent:.3f}% of {key} {disease} population must be screened to enroll target")

    if st.toggle("Show Calculation Steps"):
        st.markdown("### Calculation Breakdown")
        for category, data in [("Gender", gender_data), ("Race", race_data)]:
            st.markdown(f"**{category} Calculations**")
            for key, screened_needed, screen_percent, target_n, screen_success_rate, eligible_pop in data:
                st.text(f"{key}: Target = {target_n:.1f}, Screen Success Rate = {screen_success_rate:.2f}, Eligible Pop = {eligible_pop}, Screened Needed = {screened_needed}, Percent = {screen_percent:.3f}%")

# --- General Recruitment Strategies Section ---
st.markdown("---")
st.header(f"General Motivators and Barriers for {disease}")
st.caption("These motivators and barriers can be explored through Patient dossiers.")
if disease != "Alzheimer's":
    st.caption("Each group below includes an estimate of the % of the {disease} population that must be screened to meet enrollment targets.")

if disease == "Alzheimer's":
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("✅ Motivators")
        st.markdown("- Trusted Voices")
        st.markdown("- Altruism")
        st.markdown("- Education & Disease Awareness")
        st.markdown("- Personal Benefit")
        st.markdown("- Emphasize that memory loss is not just a part of the aging process")
        st.markdown("""
<details>
<summary><strong>Sources</strong></summary>
<a href='https://www.alz.org/help-support/resources/asian-americans-and-alzheimers' target='_blank'>Alzheimer's Association Resource</a>
</details>

<details>
<summary><strong>Solutions</strong></summary>
<a href='https://www.canva.com/design/DAGuITbntEI/jfZ6fArnWEWgH-KC9V2BNA/view?utm_content=DAGuITbntEI&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hf3030029bc' target='_blank'>Canva Educational Graphic</a>
</details>
""", unsafe_allow_html=True)

    with col2:
        st.subheader("⛔ Barriers")
        st.markdown("- Study Partner Requirement")
        st.markdown("- Procedure/Investigational Burden")
        st.markdown("- Disease Stigma")
        st.markdown("- Specific Population Injustices")

# --- Recruitment Strategies for Subgroups ---
st.markdown("---")
st.subheader(f"📣 Recruitment Strategies for Focus Populations with {disease}")

if disease == "Alzheimer's":
    st.caption("⬇️ List is in order from greatest % population needed to screen; thus greatest need to focus")

    recruitment_strategies = {
        "Asian": [
            "Emphasize that memory loss is not just a part of the aging process",
            "Provide linguistically and culturally tailored educational materials",
            "Partner with Asian community organizations and places of worship"
        ],
        "Female": [
            "Connect with women's health networks and caregiving support groups",
            "Partner with research registries",
            "Provide flexible study visit schedules or caregiver support"
        ],
        "Male": [
            "Target outreach through male-dominated environments such as sporting events",
            "Promote messaging around benefitting future generations",
            "Address stigma around mental health and participation"
        ],
        "African American": [
            "Engage trusted faith-based and civic leaders",
            "Highlight historical medical distrust and steps taken to ensure ethical practices",
            "Avoid or reassess the need for MMSE and logical memory scoring inclusion criteria as these can be inequitable barriers."
        ],
        "Hispanic": [
            "Use Spanish-language materials and bilingual coordinators",
            "Partner with local Hispanic/Latino organizations and clinics",
            "Avoid or reassess the need for MMSE and logical memory scoring as these can be barriers."
        ]
    }

    mmse_keywords = [
        "MMSE and logical memory scoring inclusion criteria",
        "MMSE and logical memory scoring"
    ]

    combined_data = gender_data + race_data
    seen = set()
    sorted_groups = []
    for group, _, screen_percent, *_ in sorted(combined_data, key=lambda x: -x[2]):
        if group not in seen:
            seen.add(group)
            sorted_groups.append(group)

    for group in sorted_groups:
        if group in recruitment_strategies:
            match = next((x for x in (gender_data + race_data) if x[0] == group), None)
            if match:
                _, _, screen_percent, *_ = match
                st.markdown(f"### {group}")
                st.caption(f"Approximately {screen_percent:.3f}% of {group} {disease} population must be screened to enroll target")
                for strategy in recruitment_strategies[group]:
                    st.markdown(f"- {strategy}", unsafe_allow_html=True)
                    if any(keyword in strategy for keyword in mmse_keywords):
                        st.markdown("""
<details>
<summary><strong>Sources</strong></summary>
<ul>
<li><a href='https://pubmed.ncbi.nlm.nih.gov/34228129/' target='_blank'>PubMed Article</a></li>
<li><a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC10171211/' target='_blank'>PMC Article</a></li>
</ul>
</details>

<details>
<summary><strong>Solutions</strong></summary>
Consider a switch of inclusion/exclusion to Montreal Cognitive Assessment (MoCA).<br>
<strong>Sources:</strong> <a href='https://pmc.ncbi.nlm.nih.gov/articles/PMC4562190/' target='_blank'>PMC Article</a>
</details>
""", unsafe_allow_html=True)
            st.markdown("---")
else:
    st.caption(f"Recruitment strategies for {disease} are currently being further explored.")
